import asyncio
import logging
import locale
from threading import Thread
from re import fullmatch
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile, Message, CallbackQuery
from aiogram.filters.command import Command

from bot.db import DB
from bot import config, kb
from bot.states import *
from bot.funcs import *

from excel.main import start_scheduler

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

db = DB()

bot = Bot(config.TOKEN)
dp = Dispatcher(storage=MemoryStorage())

weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)

with open(config.SCHEDULE_PATH, encoding='utf-8') as f:
    schedule = json.load(f)


# Главная ==============================================================================================================
@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    try:
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
    except Exception as e:
        errors.error(e)


@dp.callback_query(F.data == 'to_main')
async def call_start(call: CallbackQuery, state: FSMContext):
    try:
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
    except Exception as e:
        errors.error(e)


# Помощь ==============================================================================================================
@dp.message(Command('help'))
async def help(message: Message, state: FSMContext):
    try:
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
    except Exception as e:
        errors.error(e)


# Получить расписание ==================================================================================================
@dp.callback_query(F.data == 'get_student_schedule')
async def get_student_schedule(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        keyboard = kb.group_button(await db.get_class(str(call.from_user.id))) if await db.user_is_registered(
            str(call.from_user.id)) else kb.to_main_kb
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Введите название вашего класса (например 11с1).', reply_markup=keyboard)
        await state.set_state(GetStudentSchedule.group)
    except Exception as e:
        errors.error(e)


@dp.callback_query(GetStudentSchedule.group)
async def set_student_group(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await state.update_data(group=call.data.split('-')[1].lower())
        await bot.send_message(call.from_user.id, 'Выберите день недели.', reply_markup=kb.student_week_kb)
        await state.set_state(GetStudentSchedule.weekday)
    except Exception as e:
        errors.error(e)


@dp.message(GetStudentSchedule.group)
async def set_student_group(message: Message, state: FSMContext):
    try:
        if fullmatch(r'\d{1,2}[а-яА-Я]\d?', message.text):
            await state.update_data(group=message.text.lower())
            await message.answer('Выберите день недели.', reply_markup=kb.student_week_kb)
            await state.set_state(GetStudentSchedule.weekday)
        else:
            await message.answer('Неверный формат. Повторите ввод.')
    except Exception as e:
        errors.error(e)


@dp.callback_query(GetStudentSchedule.weekday)
@dp.callback_query(F.data.split('-')[0] == 'student')
async def set_student_weekday(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        data = await state.get_data()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=get_students_day_schedule(data['group'], call.data.split('-')[1]),
                                    parse_mode='HTML', reply_markup=kb.to_main_kb)
        await state.clear()
    except Exception as e:
        errors.error(e)


# Найти учителя ========================================================================================================
@dp.callback_query(F.data == 'find_teacher')
async def find_teacher(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Введите фамилию учителя.', reply_markup=kb.to_main_kb)
        await state.set_state(FindTeacher.teacher)
    except Exception as e:
        errors.error(e)


@dp.message(FindTeacher.teacher)
async def teacher_info(message: Message, state: FSMContext):
    try:
        flag = False
        teachers = get_teachers()
        for i, j in teachers.items():
            if message.text.lower() == j['surname'].lower():
                flag = True
                n = i
                break
        if flag:
            text = f'<b>{teachers[n]["surname"]} {teachers[n]["name"]} {teachers[n]["patronymic"]}</b>\n\n<i>Почта:</i> {teachers[n]["email"]}.\n'
            if teachers[n]['subject'] is not None:
                text += f'<i>Занимаемая должность:</i> {teachers[n]["subject"]}.'
            if teachers[n]["photo"]:
                photo = FSInputFile(f'excel/teachers/photo/{n}.jpg')
                await message.answer_photo(photo=photo, caption=text, parse_mode='HTML',
                                           reply_markup=kb.teacher_schedule_kb(message.text.capitalize()))
            else:
                await message.answer(text=text, parse_mode='HTML',
                                     reply_markup=kb.teacher_schedule_kb(message.text.capitalize()))
            await state.clear()
        else:
            await message.answer('Учитель с такой фамилией не найден. Повторите ввод.')
    except Exception as e:
        errors.error(e)


@dp.callback_query(F.data.split('-')[0] == 'teacher_schedule')
async def teacher_weekdays(call: CallbackQuery):
    try:
        await call.answer()
        await call.message.delete()
        await call.message.answer(text='Выберите день недели.',
                                  reply_markup=kb.teacher_week_kb(call.data.split('-')[1]))
    except Exception as e:
        errors.error(e)


@dp.callback_query(F.data.split('-')[0] == 'teacher')
async def get_teacher_schedule(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=get_teachers_day_schedule(call.data.split('-')[2], call.data.split('-')[1]),
                                    parse_mode='HTML', reply_markup=kb.to_teacher_schedule_kb(call.data.split('-')[2]))
    except Exception as e:
        errors.error(e)


# Предложить идею ======================================================================================================
@dp.callback_query(F.data == 'suggest_idea')
async def suggest_idea(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Если у вас есть идея по улучшению бота или школы, отправьте ее сюда (пока что поддерживаются <b>только текст и фото</b>).',
                                    parse_mode='HTML', reply_markup=kb.to_main_kb)
        await state.set_state(SuggestIdea.idea)
    except Exception as e:
        errors.error(e)


@dp.message(SuggestIdea.idea)
async def set_idea(message: Message, state: FSMContext):
    try:
        if message.photo is not None:
            if await db.user_is_registered(str(message.from_user.id)):
                await bot.send_photo(chat_id=config.IDEAS_GROUP_ID,
                                     photo=message.photo[-1].file_id,
                                     caption=f'Отправитель - @{message.from_user.username}.\n'
                                             f'Сообщение - {message.caption}.\n'
                                             f'Корпус - {await db.get_building(str(message.from_user.id))}.\n'
                                             f'Класс - {await db.get_class(str(message.from_user.id))}.',
                                     reply_markup=kb.idea_kb)
            else:
                await bot.send_photo(chat_id=config.IDEAS_GROUP_ID, photo=message.photo[-1].file_id,
                                     caption=f'Отправитель - @{message.from_user.username}.\n'
                                             f'Сообщение - {message.caption}.',
                                     reply_markup=kb.idea_kb)
            await message.answer(text='Спасибо за предложение!', reply_markup=kb.to_main_kb)
            await state.clear()
        elif message.text is not None:
            if await db.user_is_registered(str(message.from_user.id)):
                await bot.send_message(chat_id=config.IDEAS_GROUP_ID,
                                       text=f'Отправитель - @{message.from_user.username}.\n'
                                            f'Сообщение - {message.text}.\n'
                                            f'Корпус - {await db.get_building(str(message.from_user.id))}.\n'
                                            f'Класс - {await db.get_class(str(message.from_user.id))}.',
                                       reply_markup=kb.idea_kb)
            else:
                await bot.send_message(chat_id=config.IDEAS_GROUP_ID,
                                       text=f'Отправитель - @{message.from_user.username}.\n'
                                            f'Сообщение - {message.text}.',
                                       reply_markup=kb.idea_kb)
            await message.answer(text='Спасибо за предложение!', reply_markup=kb.to_main_kb)
            await state.clear()
        else:
            await message.answer(text='Этот тип контента не поддерживается. Отправьте что-нибудь другое.')
    except Exception as e:
        errors.error(e)


@dp.callback_query(F.data.split('-')[0] == 'approve_idea')
async def approve_idea(call: CallbackQuery):
    try:
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
    except Exception as e:
        errors.error(e)


# Профиль ==============================================================================================================
@dp.callback_query(F.data == 'profile')
async def profile(call: CallbackQuery):
    try:
        await call.answer()
        if await db.user_is_registered(str(call.from_user.id)):
            text = (f'Ваш корпус - {await db.get_building(str(call.from_user.id))}.\n'
                    f'Ваш класс - {await db.get_class(str(call.from_user.id))}.')
            keyboard = kb.filled_profile_kb
        else:
            text = 'Если вы ученик школы № 1580, то вы можете пройти регистрацию, чтобы не вводить каждый раз номер класса и получать новости вашего корпуса.'
            keyboard = kb.unfilled_profile_kb
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=text, reply_markup=keyboard)
    except Exception as e:
        errors.error(e)


# Регистрация ==========================================================================================================
@dp.callback_query(F.data == 'registration')
async def registration(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Выберите свой корпус.', reply_markup=kb.buildings_kb)
        await state.set_state(Registration.building)
    except Exception as e:
        errors.error(e)


@dp.callback_query(Registration.building)
async def set_registration_building(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await state.update_data(building=call.data.split('-')[1])
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Введите название вашего класса (например 11с1).')
        await state.set_state(Registration.group)
    except Exception as e:
        errors.error(e)


@dp.message(Registration.group)
async def set_registration_group(message: Message, state: FSMContext):
    try:
        await state.update_data(group=message.text)
        data = await state.get_data()
        if not fullmatch(r'\d{1,2}[а-яА-Я]\d?', message.text):
            await message.answer('Неверный формат. Повторите ввод.')
        elif schedule[data['group']]['Понедельник']['1']['building'] != data['building']:
            await message.answer('Этот класс не найден в выбранном корпусе. Повторите ввод.')
        else:
            await message.answer(
                'Спасибо за регистрацию. Теперь вы можете получить расписание вашего класса на сегодня в один клик.',
                reply_markup=kb.to_main_kb)
            await db.edit_group(str(message.from_user.id), data['group'])
            await db.edit_building(str(message.from_user.id), data['building'])
            await state.clear()
    except Exception as e:
        errors.error(e)


# Изменение класса =====================================================================================================
@dp.callback_query(F.data == 'change_group')
async def change_group(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Введите название вашего класса (например 11с1).', reply_markup=kb.to_main_kb)
        await state.set_state(ChangeGroup.group)
    except Exception as e:
        errors.error(e)


@dp.message(ChangeGroup.group)
async def set_group(message: Message, state: FSMContext):
    try:
        if not fullmatch(r'\d{1,2}[а-яА-Я]\d?', message.text):
            await message.answer('Неверный формат. Повторите ввод.')
        elif schedule[message.text]['Понедельник']['1']['building'] != await db.get_building(str(message.from_user.id)):
            await message.answer('Этот класс не найден в выбранном корпусе. Повторите ввод.')
        else:
            await message.answer('Класс изменен.', reply_markup=kb.to_main_kb)
            await db.edit_group(str(message.from_user.id), message.text)
            await state.clear()
    except Exception as e:
        errors.error(e)


# Изменение корпуса ====================================================================================================
@dp.callback_query(F.data == 'change_building')
async def change_building(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Выберите свой корпус.', reply_markup=kb.buildings_kb)
        await state.set_state(ChangeBuilding.building)
    except Exception as e:
        errors.error(e)


@dp.callback_query(ChangeBuilding.building)
async def set_building(call: CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(call.from_user.id, 'Корпус изменен.', reply_markup=kb.to_main_kb)
        await db.edit_building(str(call.from_user.id), call.data.split('-')[1])
        await state.clear()
    except Exception as e:
        errors.error(e)


# Админ панель =========================================================================================================
@dp.callback_query(lambda call: call.data == 'admin_panel')
async def admin_panel(call: CallbackQuery):
    try:
        await call.answer()
        keyboard = kb.admin_kb if await db.get_role(str(call.from_user.id)) == 'admin' else kb.newsman_kb
        text = ''
        if await db.get_role(str(call.from_user.id)) == 'admin':
            role = 'админ'
            text += f'Пользователей бота - <b>{await db.count_users()}</b>.\n'
        else:
            role = 'новостник'
        text += f'Ваша роль - <b>{role}</b>.'
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=text, reply_markup=keyboard, parse_mode='HTML')
    except Exception as e:
        errors.error(e)


# Рассылка =============================================================================================================
@dp.callback_query(lambda call: call.data == 'news')
async def message_all(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Введите сообщение.', reply_markup=kb.to_admin_panel_kb)
        await state.set_state(News.message)
    except Exception as e:
        errors.error(e)


@dp.message(News.message)
async def set_message(message: Message, state: FSMContext):
    try:
        await state.update_data(message=message.text)
        await message.answer('Выберите кому отправить сообщение.', reply_markup=kb.news_kb)
        await state.set_state(News.target)
    except Exception as e:
        errors.error(e)


@dp.callback_query(News.target)
async def set_target(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        data = await state.get_data()
        await state.update_data(target=call.data.split('-')[1])
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=f'Подтвердите отправку сообщения:\n'
                                         f'Текст - {data["message"]}.\n'
                                         f'Корпуса - {data["target"] if data["target"].isnumeric() else "все"}.',
                                    reply_markup=kb.submit_kb)
        await state.set_state(News.submit)
    except Exception as e:
        errors.error(e)


@dp.callback_query(News.submit)
async def set_submit(call: CallbackQuery, state: FSMContext):
    try:
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
    except Exception as e:
        errors.error(e)


# Выдача роли ==========================================================================================================
@dp.callback_query(lambda call: call.data == 'give_role')
async def give_role(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Введите id человека которому хотите выдать роль',
                                    reply_markup=kb.to_admin_panel_kb)
        await state.set_state(GiveRole.id)
    except Exception as e:
        errors.error(e)


@dp.message(GiveRole.id)
async def set_id(message: Message, state: FSMContext):
    try:
        if message.text in await db.get_all_users():
            await state.update_data(id=message.text)
            await message.answer('Выберите роль.', reply_markup=kb.roles_kb)
            await state.set_state(GiveRole.role)
        else:
            await message.answer('Пользователь не найден в боте. Введите id еще раз.',
                                 reply_markup=kb.to_admin_panel_kb)
    except Exception as e:
        errors.error(e)


@dp.callback_query(GiveRole.role)
async def set_role(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await state.update_data(role=call.data)
        data = await state.get_data()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Роль выдана.', reply_markup=kb.to_admin_panel_kb)
        if await db.staff_exists(data['id']):
            await db.edit_role(data['id'], data['role'], await db.get_username_by_tg(data['id']))
        else:
            await db.new_staff(data['id'], data['role'], await db.get_username_by_tg(data['id']))
        await state.clear()
    except Exception as e:
        errors.error(e)


# Кубик ================================================================================================================
@dp.message(Command('dice'))
async def dice(message: Message):
    try:
        await message.answer_dice(emoji='🎲')
    except Exception as e:
        errors.error(e)


# Слот =================================================================================================================
@dp.message(Command('slot'))
async def slot(message: Message):
    try:
        await message.answer_dice(emoji='🎰')
    except Exception as e:
        errors.error(e)


# Футбол ================================================================================================================
@dp.message(Command('football'))
async def football(message: Message):
    try:
        await message.answer_dice(emoji='⚽️')
    except Exception as e:
        errors.error(e)


# Баскетбол ================================================================================================================
@dp.message(Command('basketball'))
async def basketball(message: Message):
    try:
        await message.answer_dice(emoji='🏀')
    except Exception as e:
        errors.error(e)


# Боулинг ================================================================================================================
@dp.message(Command('bowling'))
async def bowling(message: Message):
    try:
        await message.answer_dice(emoji='🎳')
    except Exception as e:
        errors.error(e)


# Дартс ================================================================================================================
@dp.message(Command('darts'))
async def dart(message: Message):
    try:
        await message.answer_dice(emoji='🎯')
    except Exception as e:
        errors.error(e)


# Обезьяна =============================================================================================================
@dp.message(Command('monkey'))
async def monkey(message: Message):
    try:
        await message.answer_sticker('CAACAgIAAxkBAAEKc5dlHbxb-RpsaSAfgBqoQ9RE7NECXQACLA4AAns60UqyOUfKre3y0zAE')
    except Exception as e:
        errors.error(e)


# Петрикова ============================================================================================================
@dp.message(Command('petrikova'))
async def petrikova(message: Message):
    try:
        await message.answer_sticker('CAACAgIAAxkBAAEKdgxlHv4_ah2jwxqOVFWLghHRluQw4QAC0ygAArOsIEoJKU_WVCW3gTAE')
    except Exception as e:
        errors.error(e)


# 52 ===================================================================================================================
@dp.message(Command('52'))
async def fiftytwo(message: Message):
    try:
        photo = FSInputFile('mems/52.jpg')
        await message.answer_photo(photo=photo, caption='Yeei')
    except Exception as e:
        errors.error(e)


# Инвалид =============================================================================================================
@dp.message(Command('invalid'))
async def invalid(message: Message):
    try:
        photo = FSInputFile('mems/invalid.jpg')
        await message.answer_photo(photo=photo)
    except Exception as e:
        errors.error(e)


# Джакузи ==============================================================================================================
@dp.message(Command('jacuzzi'))
async def jacuzzi(message: Message):
    try:
        photo = FSInputFile('mems/jacuzzi.jpg')
        await message.answer_photo(photo=photo)
    except Exception as e:
        errors.error(e)


# Шрэк =================================================================================================================
@dp.message(Command('shrek'))
async def shrek(message: Message):
    try:
        photo = FSInputFile('mems/shrek.jpg')
        await message.answer_photo(photo=photo)
    except Exception as e:
        errors.error(e)


# id ===================================================================================================================
@dp.message(Command('id'))
async def ids(message: Message):
    try:
        await message.answer(str(message.from_user.id))
    except Exception as e:
        errors.error(e)


# group id =============================================================================================================
@dp.message(Command('gid'))
async def gids(message: Message):
    try:
        await message.answer(str(message.chat.id))
    except Exception as e:
        errors.error(e)


# all ==================================================================================================================
@dp.message()
async def all(message: Message):
    try:
        if str(message.chat.id) not in [config.IDEAS_GROUP_ID, config.APPROVED_IDEAS_GROUP_ID]:
            await message.answer('Команда не распознана. Отправьте /start для выхода в главное меню.')
    except Exception as e:
        errors.error(e)


async def main():
    await db.connect()
    Thread(target=start_scheduler).start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    print(f'Бот запущен ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')
    asyncio.run(main())
