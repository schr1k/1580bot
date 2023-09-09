from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


get_schedule = InlineKeyboardButton(text='Получить расписание', callback_data='get_schedule')
main_kb = InlineKeyboardBuilder().add(get_schedule)
