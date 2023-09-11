from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Главная ==============================================================================================================
get_schedule = InlineKeyboardButton(text='Получить расписание', callback_data='get_student_schedule')
find_teacher = InlineKeyboardButton(text='Найти учителя', callback_data='get_teacher_schedule')
main_kb = InlineKeyboardBuilder().add(get_schedule, find_teacher)


# Дни Недели для учителей ==============================================================================================
monday = InlineKeyboardButton(text='Понедельник', callback_data='teacher-Понедельник')
tuesday = InlineKeyboardButton(text='Вторник', callback_data='teacher-Вторник')
wednesday = InlineKeyboardButton(text='Среда', callback_data='teacher-Среда')
thursday = InlineKeyboardButton(text='Четверг', callback_data='teacher-Четверг')
friday = InlineKeyboardButton(text='Пятница', callback_data='teacher-Пятница')
saturday = InlineKeyboardButton(text='Суббота', callback_data='teacher-Суббота')
teacher_week_kb = InlineKeyboardBuilder().row(monday, tuesday, wednesday).row(thursday, friday, saturday)


# Дни Недели для учеников ==============================================================================================
monday = InlineKeyboardButton(text='Понедельник', callback_data='student-Понедельник')
tuesday = InlineKeyboardButton(text='Вторник', callback_data='student-Вторник')
wednesday = InlineKeyboardButton(text='Среда', callback_data='student-Среда')
thursday = InlineKeyboardButton(text='Четверг', callback_data='student-Четверг')
friday = InlineKeyboardButton(text='Пятница', callback_data='student-Пятница')
saturday = InlineKeyboardButton(text='Суббота', callback_data='student-Суббота')
student_week_kb = InlineKeyboardBuilder().row(monday, tuesday, wednesday).row(thursday, friday, saturday)
