from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config

# Назад ================================================================================================================
to_main = InlineKeyboardButton(text='🔙 На Главную', callback_data='to_main')
to_main_kb = InlineKeyboardBuilder().add(to_main).as_markup()


# Главная ==============================================================================================================
def main_kb(tg: str):
    get_schedule = InlineKeyboardButton(text='🗓 Получить расписание', callback_data='get_student_schedule')
    find_teacher = InlineKeyboardButton(text='🔍 Найти учителя', callback_data='get_teacher_schedule')
    kb = InlineKeyboardBuilder().row(get_schedule).row(find_teacher)
    if tg in config.ADMINS:
        kb.row(InlineKeyboardButton(text='👨‍💻 Админ панель', callback_data='admin_panel'))
    return kb.as_markup()


# Дни Недели для учителей ==============================================================================================
monday = InlineKeyboardButton(text='Понедельник', callback_data='teacher-Понедельник')
tuesday = InlineKeyboardButton(text='Вторник', callback_data='teacher-Вторник')
wednesday = InlineKeyboardButton(text='Среда', callback_data='teacher-Среда')
thursday = InlineKeyboardButton(text='Четверг', callback_data='teacher-Четверг')
friday = InlineKeyboardButton(text='Пятница', callback_data='teacher-Пятница')
saturday = InlineKeyboardButton(text='Суббота', callback_data='teacher-Суббота')
teacher_week_kb = InlineKeyboardBuilder().row(monday, tuesday, wednesday).row(thursday, friday, saturday).as_markup()


# Дни Недели для учеников ==============================================================================================
monday = InlineKeyboardButton(text='Понедельник', callback_data='student-Понедельник')
tuesday = InlineKeyboardButton(text='Вторник', callback_data='student-Вторник')
wednesday = InlineKeyboardButton(text='Среда', callback_data='student-Среда')
thursday = InlineKeyboardButton(text='Четверг', callback_data='student-Четверг')
friday = InlineKeyboardButton(text='Пятница', callback_data='student-Пятница')
saturday = InlineKeyboardButton(text='Суббота', callback_data='student-Суббота')
student_week_kb = InlineKeyboardBuilder().row(monday, tuesday, wednesday).row(thursday, friday, saturday).as_markup()


# Админ панель =========================================================================================================
message_all = InlineKeyboardButton(text='✉️ Рассылка', callback_data='message_all')
admin_kb = InlineKeyboardBuilder().row(message_all).row(to_main).as_markup()
