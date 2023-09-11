import asyncio
import logging
from re import fullmatch

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command

import config
import kb
from states import *
from funcs import *

bot = Bot(config.TOKEN)
dp = Dispatcher(storage=MemoryStorage())

weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

with open('excel/schedule.json', encoding='utf-8') as f:
    schedule = json.load(f)

logging.basicConfig(filename="all_log.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
warning_log = logging.getLogger("warning_log")
warning_log.setLevel(logging.WARNING)
fh = logging.FileHandler("warning_log.log")
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(funcName)s: %(message)s (%(lineno)d)')
fh.setFormatter(formatter)
warning_log.addHandler(fh)


# Главная ==============================================================================================================
@dp.message(Command('start'))
async def start(message: Message):
    try:
        name = message.from_user.username if message.from_user.username is not None else message.from_user.first_name
        await message.answer(f'👋 Привет, {name}.', reply_markup=kb.main_kb.as_markup())
    except Exception as e:
        warning_log.warning(e)


@dp.callback_query(F.data == 'to_main')
async def call_start(call: CallbackQuery):
    try:
        await call.answer()
        name = call.from_user.username if call.from_user.username is not None else call.from_user.first_name
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=f'👋 Привет, {name}.', reply_markup=kb.main_kb.as_markup())
    except Exception as e:
        warning_log.warning(e)


# Получить расписание ==================================================================================================
@dp.callback_query(F.data == 'get_student_schedule')
async def get_student_schedule(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Введите название вашего класса (например 10а1).')
        await state.set_state(GetStudentSchedule.group)
    except Exception as e:
        warning_log.warning(e)


@dp.message(GetStudentSchedule.group)
async def set_student_group(message: Message, state: FSMContext):
    try:
        print(message.text)
        if fullmatch(r'\d\d[а-яА-Я]\d', message.text):
            group = message.text[:2] + message.text[2].lower() + message.text[3]
            await state.update_data(group=group)
            await message.answer('Выберите день недели.', reply_markup=kb.student_week_kb.as_markup())
            await state.set_state(GetStudentSchedule.weekday)
        else:
            await message.answer('Класс не найден. Повторите ввод.')
    except Exception as e:
        warning_log.warning(e)


@dp.callback_query(GetStudentSchedule.weekday)
@dp.callback_query(F.data.split('-')[0] == 'student')
async def set_student_weekday(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        data = await state.get_data()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=get_student_day_schedule(data['group'], call.data.split('-')[1], '../excel/schedule.json'), parse_mode='HTML', reply_markup=kb.to_main_kb.as_markup())
        await state.clear()
    except Exception as e:
        warning_log.warning(e)


# Найти учителя ========================================================================================================
@dp.callback_query(F.data == 'get_teacher_schedule')
async def get_teacher_schedule(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text='Введите фамилию учителя.')
        await state.set_state(GetTeacherSchedule.teacher_surname)
    except Exception as e:
        warning_log.warning(e)


@dp.message(GetTeacherSchedule.teacher_surname)
async def set_teacher_surname(message: Message, state: FSMContext):
    try:
        await state.update_data(teacher=message.text)
        await message.answer('Выберите день недели.', reply_markup=kb.teacher_week_kb.as_markup())
        await state.set_state(GetTeacherSchedule.weekday)
    except Exception as e:
        warning_log.warning(e)


@dp.callback_query(GetTeacherSchedule.weekday)
@dp.callback_query(F.data.split('-')[0] == 'teacher')
async def set_teacher_weekday(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        data = await state.get_data()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=get_teachers_day_schedule(data['teacher'].capitalize(), call.data.split('-')[1], '../excel/schedule.json'), parse_mode='HTML', reply_markup=kb.to_main_kb.as_markup())
        await state.clear()
    except Exception as e:
        warning_log.warning(e)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print('Работаем')
    asyncio.run(main())
