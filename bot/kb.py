from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


get_schedule = InlineKeyboardButton(text='Получить расписание', callback_data='get_schedule')
find_teacher = InlineKeyboardButton(text='Найти учителя', callback_data='find_teacher')
monday = InlineKeyboardButton(text='Понедельник', callback_data='monday')
tuesday = InlineKeyboardButton(text='Вторник', callback_data='tuesday')
wednesday = InlineKeyboardButton(text='Среда', callback_data='wednesday')
thursday = InlineKeyboardButton(text='Четверг', callback_data='thursday')
friday = InlineKeyboardButton(text='Пятница', callback_data='friday')
saturday = InlineKeyboardButton(text='Суббота', callback_data='saturday')
main_kb = InlineKeyboardBuilder().add(get_schedule, find_teacher)
week_kb = InlineKeyboardBuilder().adjust(3).add(monday, tuesday, wednesday, thursday, friday, saturday)
