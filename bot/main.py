import asyncio
import json
import logging
from re import fullmatch

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.methods import edit_message_text

import config
import kb
from states import *

bot = Bot(config.TOKEN)
dp = Dispatcher()

with open('../excel/schedule.json', encoding='utf-8') as f:
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
        print(schedule[message.text])
        if fullmatch(r'\d\d[а-я]\d', message.text):
            await message.answer(json.dumps(schedule[message.text]['Понедельник'], ensure_ascii=False))
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
