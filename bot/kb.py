from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Главная ==============================================================================================================
get_schedule = InlineKeyboardButton(text='Получить расписание', callback_data='get_schedule')
find_teacher = InlineKeyboardButton(text='Найти учителя', callback_data='find_teacher')
main_kb = InlineKeyboardBuilder().add(get_schedule, find_teacher)


# Дни Недели ===========================================================================================================
monday = InlineKeyboardButton(text='Понедельник', callback_data='day-Понедельник')
tuesday = InlineKeyboardButton(text='Вторник', callback_data='day-Вторник')
wednesday = InlineKeyboardButton(text='Среда', callback_data='day-Среда')
thursday = InlineKeyboardButton(text='Четверг', callback_data='day-Четверг')
friday = InlineKeyboardButton(text='Пятница', callback_data='day-Пятница')
saturday = InlineKeyboardButton(text='Суббота', callback_data='day-Суббота')
week_kb = InlineKeyboardBuilder().adjust(3, 3).add(monday, tuesday, wednesday, thursday, friday, saturday)
