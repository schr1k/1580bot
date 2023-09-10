from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


get_schedule = InlineKeyboardButton(text='Получить расписание', callback_data='get_schedule')
find_teacher = InlineKeyboardButton(text='Найти учителя', callback_data='find_teacher')
monday_kb = InlineKeyboardButton(text='Понедельник', callback_data='monday_kb')
tuesday_kb = InlineKeyboardButton(text='Вторник', callback_data='tuesday_kb')
wednesday_kb = InlineKeyboardButton(text='Среда', callback_data='wednesday_kb')
thursday_kb = InlineKeyboardButton(text='Четверг', callback_data='thursday_kb')
friday_kb = InlineKeyboardButton(text='Пятница', callback_data='friday_kb')
saturday_kb = InlineKeyboardButton(text='Суббота', callback_data='saturday_kb')
main_kb = InlineKeyboardBuilder().add(get_schedule, find_teacher)
week_kb = InlineKeyboardBuilder().adjust(3).add(monday_kb, tuesday_kb, wednesday_kb, thursday_kb, friday_kb, saturday_kb)
