from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


get_schedule = InlineKeyboardButton(text='Получить расписание', callback_data='get_schedule')
find_teacher = InlineKeyboardButton(text='Найти учителя', callback_data='find_teacher')
main_kb = InlineKeyboardBuilder().add(get_schedule, find_teacher)
