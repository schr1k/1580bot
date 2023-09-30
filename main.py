import asyncio
import logging
from re import fullmatch

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command

from bot.db import DB
from bot import config, kb
from bot.states import *
from bot.funcs import *

from excel.main import main as scheduler

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
async def start(message: Message):
    try:
        if not await db.user_exists(str(message.from_user.id)):
            await db.new_user(str(message.from_user.id), message.from_user.username)
        name = message.from_user.username if message.from_user.username is not None else message.from_user.first_name
        keyboard = kb.staff_main_kb if await db.staff_exists(str(message.from_user.id)) else kb.user_main_kb
        await message.answer(f'👋 Привет, {name}.', reply_markup=keyboard)
    except Exception as e:
        errors.error(e)


@dp.callback_query(F.data == 'to_main')
async def call_start(call: CallbackQuery):
    try:
        await call.answer()
        name = call.from_user.username if call.from_user.username is not None else call.from_user.first_name
        keyboard = kb.staff_main_kb if await db.staff_exists(str(call.from_user.id)) else kb.user_main_kb
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=f'👋 Привет, {name}.', reply_markup=keyboard)
    except Exception as e:
        errors.error(e)


# Получить расписание ==================================================================================================
@dp.callback_query(F.data == 'get_student_schedule')
async def get_student_schedule(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Введите название вашего класса (например 11с1).', reply_markup=kb.to_main_kb)
        await state.set_state(GetStudentSchedule.group)
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
                                    text=get_student_day_schedule(data['group'], call.data.split('-')[1]),
                                    parse_mode='HTML', reply_markup=kb.to_main_kb)
        await state.clear()
    except Exception as e:
        errors.error(e)


# Найти учителя ========================================================================================================
@dp.callback_query(F.data == 'get_teacher_schedule')
async def get_teacher_schedule(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Введите фамилию учителя.', reply_markup=kb.to_main_kb)
        await state.set_state(GetTeacherSchedule.teacher_surname)
    except Exception as e:
        errors.error(e)


@dp.message(GetTeacherSchedule.teacher_surname)
async def set_teacher_surname(message: Message, state: FSMContext):
    try:
        await state.update_data(teacher=message.text)
        await message.answer('Выберите день недели.', reply_markup=kb.teacher_week_kb)
        await state.set_state(GetTeacherSchedule.weekday)
    except Exception as e:
        errors.error(e)


@dp.callback_query(GetTeacherSchedule.weekday)
@dp.callback_query(F.data.split('-')[0] == 'teacher')
async def set_teacher_weekday(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        data = await state.get_data()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=get_teachers_day_schedule(data['teacher'].capitalize(),
                                                                   call.data.split('-')[1]),
                                    parse_mode='HTML', reply_markup=kb.to_main_kb)
        await state.clear()
    except Exception as e:
        errors.error(e)


# Предложить идею ======================================================================================================
@dp.callback_query(F.data == 'suggest_idea')
async def suggest_idea(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Отправьте свою идею и она будет рассмотрена специальной комиссией \(||нет||\)\.',
                                    parse_mode='MarkdownV2', reply_markup=kb.to_main_kb)
        await state.set_state(SuggestIdea.idea)
    except Exception as e:
        errors.error(e)


@dp.message(SuggestIdea.idea)
async def set_idea(message: Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=config.IDEAS_GROUP_ID, text=f'Отправитель - @{message.from_user.username}\n'
                                                                   f'Сообщение - {message.text}')
        await message.answer(text='Спасибо за предложение\! Идея уже передана комиссии \(||нет||\)\.',
                             parse_mode='MarkdownV2', reply_markup=kb.to_main_kb)
        await state.clear()
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
            text = 'Если вы ученик школы № 1580, то вы можете пройти регистрацию, чтобы иметь возможность узнавать расписание на сегодня в один клик и получать новости вашего корпуса.'
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
            await message.answer('Спасибо за регистрацию. Теперь вы можете получить расписание вашего класса на сегодня в один клик.',
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
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=f'Пользователей бота - {await db.count_users()}.', reply_markup=keyboard)
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
            await message.answer('Пользователь не найден в боте. Введите id еще раз.', reply_markup=kb.to_admin_panel_kb)
    except Exception as e:
        errors.error(e)


@dp.callback_query(GiveRole.role)
async def set_role(call: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(role=call.data)
        data = await state.get_data()
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Роль выдана.', reply_markup=kb.to_admin_panel_kb)
        if await db.staff_exists(data['id']):
            await db.edit_role(data['id'], data['role'])
        else:
            await db.new_staff(data['id'], data['role'])
        await state.clear()
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


async def main():
    await db.connect()
    await dp.start_polling(bot)
    scheduler()


if __name__ == '__main__':
    print('Работаем')
    asyncio.run(main())
