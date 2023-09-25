import asyncio
import logging
from re import fullmatch

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command

from db import DB
from bot import config
import kb
from states import *
from funcs import *

db = DB()

bot = Bot(config.TOKEN)
dp = Dispatcher(storage=MemoryStorage())

weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

logging.basicConfig(filename="all.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s - (%(lineno)d)')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - (%(lineno)d)')
fh.setFormatter(formatter)
errors.addHandler(fh)


# Главная ==============================================================================================================
@dp.message(Command('start'))
async def start(message: Message):
    try:
        if not await db.user_exists(str(message.from_user.id)):
            await db.new_user(str(message.from_user.id), message.from_user.username)
        name = message.from_user.username if message.from_user.username is not None else message.from_user.first_name
        await message.answer(f'👋 Привет, {name}.', reply_markup=kb.main_kb(str(message.from_user.id)))

    except Exception as e:
        errors.error(e)


@dp.callback_query(F.data == 'to_main')
async def call_start(call: CallbackQuery):
    try:
        await call.answer()
        name = call.from_user.username if call.from_user.username is not None else call.from_user.first_name
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=f'👋 Привет, {name}.', reply_markup=kb.main_kb(str(call.from_user.id)))
    except Exception as e:
        errors.error(e)


# Получить расписание ==================================================================================================
@dp.callback_query(F.data == 'get_student_schedule')
async def get_student_schedule(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Введите название вашего класса (например 10а1).', reply_markup=kb.to_main_kb)
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
                                    text=get_teachers_day_schedule(data['teacher'].capitalize(), call.data.split('-')[1]),
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


# Админ панель =========================================================================================================
@dp.callback_query(lambda call: call.data == 'admin_panel')
async def admin_panel(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=f'Пользователей бота - {await db.count_users()}.', reply_markup=kb.admin_kb)
        await MessageAll.message.set()
    except Exception as e:
        errors.error(e)


# Рассылка =============================================================================================================
@dp.callback_query(lambda call: call.data == 'message_all')
async def message_all(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Введите сообщение.\n'
                                         '⚠️⚠️ Сообщение будет отправлено всем пользователям бота. ⚠️⚠️',
                                    reply_markup=kb.to_main_kb)
        await state.set_state(MessageAll.message)
    except Exception as e:
        errors.error(e)


@dp.message(MessageAll.message)
async def set_message(message: Message, state: FSMContext):
    try:
        for tg in await db.get_users():
            await bot.send_message(tg, message.text)
        await message.answer('Сообщение отправлено.', reply_markup=kb.to_main_kb)
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


if __name__ == "__main__":
    print('Работаем')
    asyncio.run(main())
