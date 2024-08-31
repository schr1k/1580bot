import asyncio
import locale
import logging
from datetime import datetime
from re import fullmatch

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, FSInputFile, Message
from redis.asyncio import Redis

from src.bot import kb
from src.bot.db import DB
from src.funcs import *
from src.bot.states import *
from src.main import create_schedule

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

db = DB()
config = Config()

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB
)
storage = RedisStorage(redis)

bot = Bot(config.TOKEN)
dp = Dispatcher(storage=storage)

weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)


# Главная ==============================================================================================================
@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await state.clear()
    if not await db.user_exists(str(message.from_user.id)):
        await db.new_user(str(message.from_user.id), message.from_user.username)
    name = message.from_user.username if message.from_user.username is not None else message.from_user.first_name
    keyboard = kb.staff_main_kb if await db.staff_exists(str(message.from_user.id)) else kb.user_main_kb
    now = datetime.now()
    month_day = now.strftime("%d")[1] if now.strftime("%d")[0] == '0' else now.strftime("%d")
    await message.answer(f'👋 Привет, {name}.\n'
                         f'📆 Сегодня <b>{now.strftime("%A")}</b>, {month_day} {now.strftime("%b")}.\n',
                         reply_markup=keyboard, parse_mode='HTML')


@dp.callback_query(F.data == 'to_main')
async def call_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    name = call.from_user.username if call.from_user.username is not None else call.from_user.first_name
    keyboard = kb.staff_main_kb if await db.staff_exists(str(call.from_user.id)) else kb.user_main_kb
    now = datetime.now()
    month_day = now.strftime("%d")[1] if now.strftime("%d")[0] == '0' else now.strftime("%d")
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text=f'👋 Привет, {name}.\n'
                                     f'📆 Сегодня <b>{now.strftime("%A")}</b>, {month_day} {now.strftime("%b")}.\n',
                                reply_markup=keyboard, parse_mode='HTML')


# Помощь ===============================================================================================================
@dp.message(Command('help'))
async def help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'/start - На главную.\n\n'
                         f'Приколы:\n'
                         f'/dice - кубик.\n'
                         f'/slot - слоты.\n'
                         f'/football - футбол.\n'
                         f'/basketball - баскетбол.\n'
                         f'/bowling - боулинг.\n'
                         f'/darts - дартс.\n\n'
                         f'Контакты:\n'
                         f'@schr1k - <b>CEO, CTO, CIO, Founder, TeamLead, Главный Разработчик</b>.\n'
                         f'@hxllmvdx - <i>разработчик</i>.', reply_markup=kb.to_main_kb, parse_mode='HTML')


# Получить расписание ==================================================================================================
@dp.callback_query(F.data == 'get_student_schedule')
async def get_student_schedule(call: CallbackQuery, state: FSMContext):
    await call.answer()
    keyboard = kb.group_button(await db.get_group(str(call.from_user.id))) if await db.user_is_registered(
        str(call.from_user.id)) else kb.to_main_kb
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='Введите название вашего класса (например 11с1).', reply_markup=keyboard)
    await state.set_state(GetStudentSchedule.group)


@dp.message(GetStudentSchedule.group)
async def student_weekday(message: Message, state: FSMContext):
    if fullmatch(r'\d{1,2}[а-яА-Я]\d?', message.text):
        if message.text in get_schedule().keys():
            await message.answer('Выберите день недели.', reply_markup=kb.student_week_kb(message.text.lower()))
            await state.clear()
        else:
            await message.answer('Класс не найден. Повторите ввод.')
    else:
        await message.answer('Неверный формат. Повторите ввод.')


@dp.callback_query(F.data.split('-')[0] == 'group_button')
async def call_student_weekday(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='Выберите день недели.',
                                reply_markup=kb.student_week_kb(call.data.split('-')[1].lower()))
    await state.clear()


@dp.callback_query(F.data.split('-')[0] == 'student')
async def get_student_weekday_schedule(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text=get_students_day_schedule(call.data.split('-')[2].lower(),
                                                               call.data.split('-')[1]), parse_mode='HTML',
                                reply_markup=kb.to_student_schedule_kb(call.data.split('-')[2].lower()))


# Найти учителя ========================================================================================================
@dp.callback_query(F.data == 'find_teacher')
async def find_teacher(call: CallbackQuery, state: FSMContext):
    await call.answer()
    keyboard = kb.teacher_button(await db.get_teacher(str(call.from_user.id))) if await db.get_teacher(
        str(call.from_user.id)) is not None else kb.to_main_kb
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='Введите инициалы учителя.\n'
                                     'Сейчас доступно 3 режима поиска:\n'
                                     '1) Полное ФИО (Иванов Иван Иванович).\n'
                                     '2) Фамилия и имя (Иванов Иван).\n'
                                     '3) Фамилия (Иванов).\n'
                                     '<b>Регистр при вводе не учитывается</b>.', parse_mode='HTML',
                                reply_markup=keyboard)
    await state.set_state(FindTeacher.teacher)


@dp.message(FindTeacher.teacher)
async def teacher_info(message: Message, state: FSMContext):
    flag = False
    n = 0
    teachers = get_teachers()
    if len(message.text.split()) == 3:
        surname, name, patronymic = message.text.split()
        for i, j in teachers.items():
            if surname.lower() == j['surname'].lower() and name.lower() == j['name'].lower() and patronymic.lower() == j['patronymic'].lower():
                flag = True
                n = i
                break
    elif len(message.text.split()) == 2:
        surname, name = message.text.split()
        for i, j in teachers.items():
            if surname.lower() == j['surname'].lower() and name.lower() == j['name'].lower():
                flag = True
                n = i
                break
    elif len(message.text.split()) == 1:
        surname = message.text
        for i, j in teachers.items():
            if surname.lower() == j['surname'].lower():
                flag = True
                n = i
                break
    else:
        await message.answer('Неверный формат. Повторите ввод.')
        return
    if flag:
        text = f'<b>{teachers[n]["surname"]} {teachers[n]["name"]} {teachers[n]["patronymic"]}</b>\n\n<i>Почта:</i> {teachers[n]["email"]}.\n'
        if teachers[n]['subject'] is not None:
            text += f'<i>Занимаемая должность:</i> {teachers[n]["subject"]}.'
        if teachers[n]["photo"]:
            photo = FSInputFile(f'public/photo/photo/{n}.jpg')
            await message.answer_photo(photo=photo, caption=text, parse_mode='HTML',
                                       reply_markup=kb.teacher_schedule_kb(message.text.split()[0].capitalize()))
        else:
            await message.answer(text=text, parse_mode='HTML',
                                 reply_markup=kb.teacher_schedule_kb(message.text.split()[0].capitalize()))
        await state.clear()
    else:
        await message.answer('Учитель не найден. Повторите ввод.')


@dp.callback_query(F.data.split('-')[0] == 'teacher_button')
async def call_teacher_info(call: CallbackQuery):
    await call.answer()
    flag = False
    n = 0
    teachers = get_teachers()
    surname = call.data.split('-')[1]
    for i, j in teachers.items():
        if surname.lower() == j['surname'].lower():
            flag = True
            n = i
            break
    if not flag:
        await call.message.answer(text='Учитель не найден. Измените фамилию учителя в профиле.',
                                  reply_markup=kb.to_main_kb)
    text = f'<b>{teachers[n]["surname"]} {teachers[n]["name"]} {teachers[n]["patronymic"]}</b>\n\n<i>Почта:</i> {teachers[n]["email"]}.\n'
    if teachers[n]['subject'] is not None:
        text += f'<i>Занимаемая должность:</i> {teachers[n]["subject"]}.'
    if teachers[n]["photo"]:
        photo = FSInputFile(f'public/photo/photo/{n}.jpg')
        await call.message.answer_photo(photo=photo, caption=text, parse_mode='HTML',
                                        reply_markup=kb.teacher_schedule_kb(call.data.split('-')[1]))
    else:
        await call.message.answer(text=text, parse_mode='HTML',
                                  reply_markup=kb.teacher_schedule_kb(call.data.split('-')[1]))


@dp.callback_query(F.data.split('-')[0] == 'teacher_schedule')
async def teacher_weekdays(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text='Выберите день недели.',
                              reply_markup=kb.teacher_week_kb(call.data.split('-')[1]))


@dp.callback_query(F.data.split('-')[0] == 'teacher')
async def get_teacher_schedule(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text=get_teachers_day_schedule(call.data.split('-')[2], call.data.split('-')[1]),
                                parse_mode='HTML', reply_markup=kb.to_teacher_schedule_kb(call.data.split('-')[2]))


# Предложить идею ======================================================================================================
@dp.callback_query(F.data == 'suggest_idea')
async def suggest_idea(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='Если у вас есть идея по улучшению бота или школы, отправьте ее сюда (пока что поддерживаются <b>только текст и фото</b>).',
                                parse_mode='HTML', reply_markup=kb.to_main_kb)
    await state.set_state(SuggestIdea.idea)


@dp.message(SuggestIdea.idea)
async def set_idea(message: Message, state: FSMContext):
    sender = f'@{message.from_user.username}' if message.from_user.username is not None else message.from_user.id
    if message.photo is not None:
        if await db.user_is_registered(str(message.from_user.id)):
            await bot.send_photo(chat_id=config.IDEAS_GROUP_ID, photo=message.photo[-1].file_id,
                                 caption=f'Отправитель - {sender}.\n'
                                         f'Сообщение - {message.caption}.\n'
                                         f'Корпус - {await db.get_building(str(message.from_user.id))}.\n'
                                         f'Класс - {await db.get_group(str(message.from_user.id))}.',
                                 reply_markup=kb.idea_kb)
        else:
            await bot.send_photo(chat_id=config.IDEAS_GROUP_ID, photo=message.photo[-1].file_id,
                                 caption=f'Отправитель - {sender}.\n'
                                         f'Сообщение - {message.caption}.', reply_markup=kb.idea_kb)
        await message.answer(text='Спасибо за предложение!', reply_markup=kb.to_main_kb)
        await state.clear()
    elif message.text is not None:
        if await db.user_is_registered(str(message.from_user.id)):
            await bot.send_message(chat_id=config.IDEAS_GROUP_ID, text=f'Отправитель - {sender}.\n'
                                                                       f'Сообщение - {message.text}.\n'
                                                                       f'Корпус - {await db.get_building(str(message.from_user.id))}.\n'
                                                                       f'Класс - {await db.get_group(str(message.from_user.id))}.',
                                   reply_markup=kb.idea_kb)
        else:
            await bot.send_message(chat_id=config.IDEAS_GROUP_ID, text=f'Отправитель - {sender}.\n'
                                                                       f'Сообщение - {message.text}.',
                                   reply_markup=kb.idea_kb)
        await message.answer(text='Спасибо за предложение!', reply_markup=kb.to_main_kb)
        await state.clear()
    else:
        await message.answer(text='Этот тип контента не поддерживается. Отправьте что-нибудь другое.')


@dp.callback_query(F.data.split('-')[0] == 'approve_idea')
async def approve_idea(call: CallbackQuery):
    await call.answer()
    if call.message.photo is not None:
        await bot.send_photo(chat_id=config.APPROVED_IDEAS_GROUP_ID, photo=call.message.photo[-1].file_id,
                             caption=f'{call.message.caption}')
        await bot.edit_message_caption(message_id=call.message.message_id, chat_id=config.IDEAS_GROUP_ID,
                                       caption=f'{call.message.caption}\n'
                                               f'Идея одобрена.')
    elif call.message.text is not None:
        await bot.send_message(chat_id=config.APPROVED_IDEAS_GROUP_ID, text=f'{call.message.text}')
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=config.IDEAS_GROUP_ID,
                                    text=f'{call.message.text}\n'
                                         f'Идея одобрена.')
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Произошла ошибка')


# Сообщить об ошибке ===================================================================================================
@dp.callback_query(F.data == 'report_bug')
async def report_bug(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='Если вы обнаружили ошибку или недочет при использовании бота, напишите нам об этом (пожалуйста по возможности прикладывайте скриншот чтобы мы понимали где конкретно произошла ошибка).',
                                parse_mode='HTML', reply_markup=kb.to_main_kb)
    await state.set_state(ReportBug.bug)


@dp.message(ReportBug.bug)
async def set_bug(message: Message, state: FSMContext):
    sender = f'@{message.from_user.username}' if message.from_user.username is not None else message.from_user.id
    if message.photo is not None:
        if await db.user_is_registered(str(message.from_user.id)):
            await bot.send_photo(chat_id=config.BUGS_GROUP_ID, photo=message.photo[-1].file_id,
                                 caption=f'Отправитель - {sender}.\n'
                                         f'Сообщение - {message.caption}.\n'
                                         f'Корпус - {await db.get_building(str(message.from_user.id))}.\n'
                                         f'Класс - {await db.get_group(str(message.from_user.id))}.',
                                 reply_markup=kb.bug_kb(str(message.from_user.id)))
        else:
            await bot.send_photo(chat_id=config.BUGS_GROUP_ID, photo=message.photo[-1].file_id,
                                 caption=f'Отправитель - {sender}.\n'
                                         f'Сообщение - {message.caption}.',
                                 reply_markup=kb.bug_kb(str(message.from_user.id)))
        await message.answer(text='Спасибо за помощь!\n'
                                  'Мы сообщим вам когда ошибка будет исправлена.', reply_markup=kb.to_main_kb)
        await state.clear()
    elif message.text is not None:
        if await db.user_is_registered(str(message.from_user.id)):
            await bot.send_message(chat_id=config.BUGS_GROUP_ID, text=f'Отправитель - {sender}.\n'
                                                                      f'Сообщение - {message.text}.\n'
                                                                      f'Корпус - {await db.get_building(str(message.from_user.id))}.\n'
                                                                      f'Класс - {await db.get_group(str(message.from_user.id))}.',
                                   reply_markup=kb.bug_kb(str(message.from_user.id)))
        else:
            await bot.send_message(chat_id=config.BUGS_GROUP_ID, text=f'Отправитель - {sender}.\n'
                                                                      f'Сообщение - {message.text}.',
                                   reply_markup=kb.bug_kb(str(message.from_user.id)))
        await message.answer(text='Спасибо за помощь!\n'
                                  'Мы сообщим вам когда ошибка будет исправлена.', reply_markup=kb.to_main_kb)
        await state.clear()
    else:
        await message.answer(text='Этот тип контента не поддерживается. Отправьте что-нибудь другое.')


@dp.callback_query(F.data.split('-')[0] == 'fix_bug')
async def fix_bug(call: CallbackQuery):
    await call.answer()
    if call.message.photo is not None:
        await bot.send_message(chat_id=call.data.split('-')[1],
                               text='Ошибка, о которой вы ранее сообщали, была исправлена.')
        await bot.edit_message_caption(message_id=call.message.message_id, chat_id=config.BUGS_GROUP_ID,
                                       caption=f'{call.message.caption}\n'
                                               f'Баг пофикшен.')
    elif call.message.text is not None:
        await bot.send_message(chat_id=call.data.split('-')[1],
                               text='Ошибка, о которой вы ранее сообщали, была исправлена.')
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=config.BUGS_GROUP_ID,
                                    text=f'{call.message.text}\n'
                                         f'Баг пофикшен.')
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Произошла ошибка')


@dp.callback_query(F.data.split('-')[0] == 'reject_bug')
async def reject_bug(call: CallbackQuery):
    await call.answer()
    if call.message.photo is not None:
        await bot.send_message(chat_id=call.data.split('-')[1],
                               text='Ошибка, о которой вы ранее сообщали, не была исправлена.\n'
                                    'Скорее всего разработчики не поняли где находится ошибка.\n'
                                    'Попробуйте еще раз и обязательно приложите скриншот.')
        await bot.edit_message_caption(message_id=call.message.message_id, chat_id=config.BUGS_GROUP_ID,
                                       caption=f'{call.message.caption}\n'
                                               f'Баг отклонен.')
    elif call.message.text is not None:
        await bot.send_message(chat_id=call.data.split('-')[1],
                               text='Ошибка, о которой вы ранее сообщали, не была исправлена.\n'
                                    'Скорее всего разработчики не поняли где находится ошибка.\n'
                                    'Попробуйте еще раз и обязательно приложите скриншот.')
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=config.BUGS_GROUP_ID,
                                    text=f'{call.message.text}\n'
                                         f'Баг отклонен.')
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Произошла ошибка')


# Профиль ==============================================================================================================
@dp.callback_query(F.data == 'profile')
async def profile(call: CallbackQuery):
    await call.answer()
    building = await db.get_building(str(call.from_user.id))
    group = await db.get_group(str(call.from_user.id))
    teacher = await db.get_teacher(str(call.from_user.id))
    if await db.user_is_registered(str(call.from_user.id)):
        text = (f'Ваш корпус - {building if building is not None else "Не указан"}.\n'
                f'Ваш класс - {group if group is not None else "Не указан"}.\n'
                f'Ваш учитель - {teacher if teacher is not None else "Не указан"}.')
        keyboard = kb.filled_profile_kb
    else:
        text = 'Если вы ученик школы № 1580, то вы можете пройти регистрацию, чтобы не вводить каждый раз номер класса и получать новости вашего корпуса.'
        keyboard = kb.unfilled_profile_kb
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=text,
                                reply_markup=keyboard)


# Регистрация ==========================================================================================================
@dp.callback_query(F.data == 'registration')
async def registration(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='Выберите свой корпус.', reply_markup=kb.buildings_kb)
    await state.set_state(Registration.building)


@dp.callback_query(Registration.building)
async def set_registration_building(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(building=call.data.split('-')[1])
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='Введите название вашего класса (например 11с1).')
    await state.set_state(Registration.group)


@dp.message(Registration.group)
async def set_registration_group(message: Message, state: FSMContext):
    data = await state.get_data()
    schedule = get_schedule()
    if not bool(fullmatch(r'\d{1,2}[а-яА-Я]\d?', message.text)):
        await message.answer(text='Неверный формат. Повторите ввод.')
    elif schedule[message.text.lower()]['Понедельник']['1']['building'] != data['building']:
        await message.answer(text='Этот класс не найден в выбранном корпусе. Повторите ввод.')
    else:
        await state.update_data(group=message.text)
        await message.answer(text='Введите фамилию вашего классного руководителя\n'
                                  '<b>Регистр при вводе не учитывается</b>.',
                             parse_mode='HTML')
        await state.set_state(Registration.teacher)


@dp.message(Registration.teacher)
async def set_registration_teacher(message: Message, state: FSMContext):
    if len(message.text.split(' ')) != 1:
        await message.answer(text='Неверный формат. Повторите ввод.')
    teachers = get_teachers()
    flag = False
    surname = message.text
    for i, j in teachers.items():
        if surname.lower() == j['surname'].lower():
            flag = True
            break
    if not flag:
        await message.answer(text='Учитель не найден. Повторите ввод.')
    await state.update_data(teacher=message.text.capitalize())
    data = await state.get_data()
    await message.answer(
        text='Спасибо за регистрацию. Теперь вы можете получить расписание вашего класса или вашего классного руководителя в один клик.',
        reply_markup=kb.to_main_kb)
    await db.edit_group(str(message.from_user.id), data['group'])
    await db.edit_building(str(message.from_user.id), data['building'])
    await db.edit_teacher(str(message.from_user.id), data['teacher'])
    await state.clear()


# Изменение класса =====================================================================================================
@dp.callback_query(F.data == 'change_group')
async def change_group(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='Введите название вашего класса (например 11с1).', reply_markup=kb.to_main_kb)
    await state.set_state(ChangeGroup.group)


@dp.message(ChangeGroup.group)
async def set_group(message: Message, state: FSMContext):
    schedule = get_schedule()
    if not fullmatch(r'\d{1,2}[а-яА-Я]\d?', message.text):
        await message.answer('Неверный формат. Повторите ввод.')
    elif schedule[message.text]['Понедельник']['1']['building'] != await db.get_building(str(message.from_user.id)):
        await message.answer('Этот класс не найден в выбранном корпусе. Повторите ввод.')
    else:
        await message.answer('Класс изменен.', reply_markup=kb.to_main_kb)
        await db.edit_group(str(message.from_user.id), message.text)
        await state.clear()


# Изменение корпуса ====================================================================================================
@dp.callback_query(F.data == 'change_building')
async def change_building(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='Выберите свой корпус.', reply_markup=kb.buildings_kb)
    await state.set_state(ChangeBuilding.building)


@dp.callback_query(ChangeBuilding.building)
async def set_building(call: CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, 'Корпус изменен.', reply_markup=kb.to_main_kb)
    await db.edit_building(str(call.from_user.id), call.data.split('-')[1])
    await state.clear()


# Изменение классного руководителя =====================================================================================
@dp.callback_query(F.data == 'change_teacher')
async def change_teacher(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='Введите фамилию вашего классного руководителя\n'
                                     '<b>Регистр при вводе не учитывается</b>.',
                                parse_mode='HTML')
    await state.set_state(ChangeTeacher.teacher)


@dp.message(ChangeTeacher.teacher)
async def set_teacher(message: Message, state: FSMContext):
    if len(message.text.split(' ')) != 1:
        await message.answer(text='Неверный формат. Повторите ввод.')
    teachers = get_teachers()
    flag = False
    surname = message.text
    for i, j in teachers.items():
        if surname.lower() == j['surname'].lower():
            flag = True
            break
    if not flag:
        await message.answer(text='Учитель не найден. Повторите ввод.')
    await db.edit_teacher(str(message.from_user.id), message.text.capitalize())
    await message.answer('Классный руководитель изменен.', reply_markup=kb.to_main_kb)
    await state.clear()


# Школа ================================================================================================================
@dp.callback_query(F.data == 'school')
async def school(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                text='График работы администрации школы: 09:00 - 17:30 (обед 13:15 - 13:45).',
                                reply_markup=kb.school_kb)


# Питание ==============================================================================================================
@dp.callback_query(F.data == 'food')
async def food(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
    await call.message.answer(text='График работы столовой:\n'
                                   '<b>09:00 - 14:15</b>.\n'
                                   'График работы буфета:\n'
                                   '<b>09:00 – 15:45</b>.', reply_markup=kb.food_kb, parse_mode='HTML')


# Меню =================================================================================================================
@dp.callback_query(F.data.split('-')[0] == 'menu')
async def menu(call: CallbackQuery):
    await call.answer()
    photo = FSInputFile(f'public/photo/food/{call.data.split("-")[1]}.jpg')
    await call.message.answer_photo(photo=photo, reply_markup=kb.to_food_kb)
    await call.message.delete()


# Библиотека ===========================================================================================================
@dp.callback_query(F.data == 'library')
async def library(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Библиотека ГБОУ "Бауманская инженерная школа № 1580" была основана при открытии школы в 1989 году. Основной фонд составляет 15 318 экземпляров, фонд учебной литературы – 84 257 экземпляров, периодические издания. Заведующая библиотекой - Стрекалова Марина Борисовна.',
                                reply_markup=kb.library_kb)


@dp.callback_query(F.data == 'library_1')
async def library_1(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Адрес: Балаклавский проспект, д. 6а (1 этаж, каб. 116).\n'
                                     'Телефон: 8(495)316-50-36.\n'
                                     'Режим работы: 09:00 - 17:00. Пн - Пт.', reply_markup=kb.to_library_kb)


@dp.callback_query(F.data == 'library_2')
async def library_2(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Адрес: Балаклавский проспект, д. 6 (1 этаж, каб. 104).\n'
                                     'Телефон: 8(499)619-39-35.\n'
                                     'Режим работы: 09:00 - 17:00. Пн - Пт.', reply_markup=kb.to_library_kb)


@dp.callback_query(F.data == 'library_3')
async def library_3(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Адрес: ул. Стасовой, д. 8 (4 этаж, каб. 418).\n'
                                     'Телефон: 8(495)954-34-95.\n'
                                     'Режим работы: 09:00 - 17:00. Пн - Пт.', reply_markup=kb.to_library_kb)


# Звонки ===============================================================================================================
@dp.callback_query(F.data == 'lessons')
async def lessons(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='0 урок: 08:15 - 08:55.\n'
                                     '1 урок: 09:00 - 09:40.\n'
                                     '2 урок: 09:50 - 10:30.\n'
                                     '3 урок: 10:45 - 11:25.\n'
                                     '4 урок: 11:40 - 12:20.\n'
                                     '5 урок: 12:40 - 13:20.\n'
                                     '6 урок: 13:40 - 14:20.\n'
                                     '7 урок: 14:40 - 15:20.\n'
                                     '8 урок: 15:30 - 16:10.', reply_markup=kb.to_school_kb)


# Админ панель =========================================================================================================
@dp.callback_query(lambda call: call.data == 'admin_panel')
async def admin_panel(call: CallbackQuery):
    await call.answer()
    keyboard = kb.admin_kb if await db.get_role(str(call.from_user.id)) == 'admin' else kb.newsman_kb
    text = ''
    if await db.get_role(str(call.from_user.id)) == 'admin':
        role = 'админ'
        text += (f'Всего пользователей бота - <b>{await db.count_users()}</b>.\n'
                 f'Зарегистрировано - <b>{await db.count_registered_users()}</b>.\n'
                 f'Работников - <b>{await db.count_staff()}</b>.\n')
    else:
        role = 'новостник'
    text += f'Ваша роль - <b>{role}</b>.'
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                reply_markup=keyboard, parse_mode='HTML')


# Рассылка =============================================================================================================
@dp.callback_query(lambda call: call.data == 'news')
async def message_all(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Введите сообщение.', reply_markup=kb.to_admin_panel_kb)
    await state.set_state(News.message)


@dp.message(News.message)
async def set_message(message: Message, state: FSMContext):
    await state.update_data(message=message.text)
    await message.answer('Выберите кому отправить сообщение.', reply_markup=kb.news_kb)
    await state.set_state(News.target)


@dp.callback_query(News.target)
async def set_target(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(target=call.data.split("-")[1])
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text=f'Подтвердите отправку сообщения:\n'
                                     f'Текст - {data["message"]}\n'
                                     f'Корпуса - {call.data.split("-")[1] if call.data.split("-")[1].isnumeric() else "все (все пользователи бота)"}.',
                                reply_markup=kb.submit_kb)
    await state.set_state(News.submit)


@dp.callback_query(News.submit)
async def set_submit(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    if data['target'].isnumeric():
        message_list = await db.get_users_by_building(data['target'])
    else:
        message_list = await db.get_all_users()
    for user in message_list:
        await bot.send_message(user, data['message'])
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Сообщение отправлено.', reply_markup=kb.to_admin_panel_kb)
    await state.clear()


# Выдача роли ==========================================================================================================
@dp.callback_query(lambda call: call.data == 'give_role')
async def give_role(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Введите id человека которому хотите выдать роль',
                                reply_markup=kb.to_admin_panel_kb)
    await state.set_state(GiveRole.id)


@dp.message(GiveRole.id)
async def set_id(message: Message, state: FSMContext):
    if message.text in await db.get_all_users():
        await state.update_data(id=message.text)
        await message.answer('Выберите роль.', reply_markup=kb.roles_kb)
        await state.set_state(GiveRole.role)
    else:
        await message.answer('Пользователь не найден в боте. Введите id еще раз.',
                             reply_markup=kb.to_admin_panel_kb)


@dp.callback_query(GiveRole.role)
async def set_role(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(role=call.data)
    data = await state.get_data()
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Роль выдана.',
                                reply_markup=kb.to_admin_panel_kb)
    if await db.staff_exists(data['id']):
        await db.edit_role(data['id'], data['role'], await db.get_username_by_tg(data['id']))
    else:
        await db.new_staff(data['id'], data['role'], await db.get_username_by_tg(data['id']))
    await state.clear()


# Кубик ================================================================================================================
@dp.message(Command('dice'))
async def dice(message: Message):
    await message.answer_dice(emoji='🎲')


# Слот =================================================================================================================
@dp.message(Command('slot'))
async def slot(message: Message):
    await message.answer_dice(emoji='🎰')


# Футбол ===============================================================================================================
@dp.message(Command('football'))
async def football(message: Message):
    await message.answer_dice(emoji='⚽️')


# Баскетбол ============================================================================================================
@dp.message(Command('basketball'))
async def basketball(message: Message):
    await message.answer_dice(emoji='🏀')


# Боулинг ==============================================================================================================
@dp.message(Command('bowling'))
async def bowling(message: Message):
    await message.answer_dice(emoji='🎳')


# Дартс ================================================================================================================
@dp.message(Command('darts'))
async def dart(message: Message):
    await message.answer_dice(emoji='🎯')


# Обезьяна =============================================================================================================
@dp.message(Command('monkey'))
async def monkey(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAEKc5dlHbxb-RpsaSAfgBqoQ9RE7NECXQACLA4AAns60UqyOUfKre3y0zAE')


# Петрикова ============================================================================================================
@dp.message(Command('petrikova'))
async def petrikova(message: Message):
    await message.answer_sticker('CAACAgIAAxkBAAEKdgxlHv4_ah2jwxqOVFWLghHRluQw4QAC0ygAArOsIEoJKU_WVCW3gTAE')


# 52 ===================================================================================================================
@dp.message(Command('52'))
async def fiftytwo(message: Message):
    photo = FSInputFile('public/photo/mems/52.jpg')
    await message.answer_photo(photo=photo, caption='Yeei')


# Инвалид =============================================================================================================
@dp.message(Command('invalid'))
async def invalid(message: Message):
    photo = FSInputFile('public/photo/mems/invalid.jpg')
    await message.answer_photo(photo=photo)


# Джакузи ==============================================================================================================
@dp.message(Command('jacuzzi'))
async def jacuzzi(message: Message):
    photo = FSInputFile('public/photo/mems/jacuzzi.jpg')
    await message.answer_photo(photo=photo)


# Шрэк =================================================================================================================
@dp.message(Command('shrek'))
async def shrek(message: Message):
    photo = FSInputFile('public/photo/mems/shrek.jpg')
    await message.answer_photo(photo=photo)


# id ===================================================================================================================
@dp.message(Command('id'))
async def ids(message: Message):
    await message.answer(str(message.from_user.id))


# group id =============================================================================================================
@dp.message(Command('gid'))
async def gids(message: Message):
    await message.answer(str(message.chat.id))


# command_exception ====================================================================================================
@dp.message()
async def command_exception(message: Message):
    if str(message.chat.id) not in [config.IDEAS_GROUP_ID, config.APPROVED_IDEAS_GROUP_ID, config.BUGS_GROUP_ID]:
        await message.answer('Команда не распознана. Отправьте /start для выхода в главное меню.')


async def main():
    try:
        await db.connect()
        await asyncio.create_task(create_schedule())
        print(f'Бот запущен ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')
        await dp.start_polling(bot)
    except Exception as e:
        errors.error(e)


if __name__ == '__main__':
    asyncio.run(main())
