import asyncio
import logging
from re import fullmatch

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command

import config
import kb
from states import *
from bot.funcs import *

bot = Bot(config.TOKEN)
dp = Dispatcher()

with open('..\\excel\\1\\schedule1.json', encoding='utf-8') as f:
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
        await message.answer('Ку', reply_markup=kb.main_kb.as_markup())
    except Exception as e:
        warning_log.warning(e)


@dp.callback_query(F.data == 'find_teacher')
async def get_teachers_name(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,text='Введите фамилию учителя')
        await state.set_state(GetTeachersSchedule.teachers_name)
    except Exception as e:
        warning_log.warning(e)


@dp.message(GetTeachersSchedule.teachers_name)
async def chose_weekday(message: Message, state: FSMContext):
    try:
        await state.update_data(teacher=message.text)
        await message.answer('Выберите день недели', reply_markup=kb.week_kb.as_markup())
    except Exception as e:
        warning_log.warning(e)


@dp.callback_query(F.data.split('-')[0] == 'day')
async def get_teachers_schedule(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        data = await state.get_data()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                    text=get_teachers_day_schedule(data['teacher'], F.data.split('-')[1], '..\\excel\\1\\schedule1.json'))
        await state.clear()
    except Exception as e:
        warning_log.warning(e)


@dp.callback_query(F.data == 'get_schedule')
async def get_schedule(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text='Введите название вашего класса (например 10а1)')
        await state.set_state(GetSchedule.group)
    except Exception as e:
        warning_log.warning(e)


@dp.message(GetSchedule.group)
async def send_schedule(message: Message, state: FSMContext):
    try:
        if fullmatch(r'\d\d[а-я]\d', message.text):
            await message.answer(get_day_schedule(message.text, 'Понедельник', '..\\excel\\1\\schedule1.json'))
            await state.clear()
        else:
            await message.answer('Неправильный формат. Введите класс еще раз.')
    except Exception as e:
        warning_log.warning(e)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    print('Работаем')
    asyncio.run(main())
