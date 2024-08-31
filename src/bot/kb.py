from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

to_main = InlineKeyboardButton(text='🔙 На Главную', callback_data='to_main')
to_main_kb = InlineKeyboardBuilder().add(to_main).as_markup()

to_school = InlineKeyboardButton(text='🔙 Школа', callback_data='school')
to_school_kb = InlineKeyboardBuilder().add(to_school).as_markup()

to_teacher = InlineKeyboardButton(text='🔙 Поиск', callback_data='find_teacher')
to_teacher_kb = InlineKeyboardBuilder().add(to_teacher).as_markup()

to_group = InlineKeyboardButton(text='🔙 Поиск', callback_data='get_student_schedule')
to_group_kb = InlineKeyboardBuilder().add(to_group).as_markup()

to_food = InlineKeyboardButton(text='🔙 Питание', callback_data='food')
to_food_kb = InlineKeyboardBuilder().add(to_food).as_markup()

to_library = InlineKeyboardButton(text='🔙 Библиотека', callback_data='library')
to_library_kb = InlineKeyboardBuilder().add(to_library).as_markup()

to_admin_panel = InlineKeyboardButton(text='🔙 Админ-панель', callback_data='admin_panel')
to_admin_panel_kb = InlineKeyboardBuilder().add(to_admin_panel).as_markup()

get_schedule = InlineKeyboardButton(text='🗓 Получить расписание', callback_data='get_student_schedule')
find_teacher = InlineKeyboardButton(text='🔍 Найти учителя', callback_data='find_teacher')
suggest_idea = InlineKeyboardButton(text='💡 Предложить идею', callback_data='suggest_idea')
report_bug = InlineKeyboardButton(text='⛔️ Сообщить об ошибке', callback_data='report_bug')
profile = InlineKeyboardButton(text='👤 Профиль', callback_data='profile')
school = InlineKeyboardButton(text='ℹ️ Школа', callback_data='school')
user_main_kb = InlineKeyboardBuilder().row(get_schedule).row(find_teacher).row(suggest_idea).row(report_bug).row(
    profile, school).as_markup()

admin_panel = InlineKeyboardButton(text='👨‍💻 Админ панель', callback_data='admin_panel')
staff_main_kb = InlineKeyboardBuilder().row(get_schedule).row(find_teacher).row(suggest_idea).row(report_bug).row(
    profile, school).row(admin_panel).as_markup()


def teacher_schedule_kb(teacher: str) -> InlineKeyboardMarkup:
    """
    Make keyboard with "get schedule" button for provided teacher.
    :param teacher: Teacher's surname
    :return: :class:`InlineKeyboardMarkup`: Keyboard with "get schedule" button for provided teacher
    """
    teacher_schedule = InlineKeyboardButton(text='📅 Узнать расписание', callback_data=f'teacher_schedule-{teacher}')
    keyboard = InlineKeyboardBuilder().row(teacher_schedule).as_markup()
    return keyboard


def to_teacher_schedule_kb(teacher: str) -> InlineKeyboardMarkup:
    """
    Make keyboard with "go to teacher's profile" button for provided teacher.
    :param teacher: Teacher's surname
    :return: :class:`InlineKeyboardMarkup`: Keyboard with "go to teachers profile" button for provided teacher
    """
    teacher_schedule = InlineKeyboardButton(text='🔙 Назад', callback_data=f'teacher_schedule-{teacher}')
    keyboard = InlineKeyboardBuilder().row(teacher_schedule).as_markup()
    return keyboard


def teacher_week_kb(teacher: str) -> InlineKeyboardMarkup:
    """
    Make keyboard with weekdays buttons for provided teacher.
    :param teacher: Teacher's surname
    :return: :class:`InlineKeyboardMarkup`: Keyboard with weekdays buttons for provided teacher
    """
    monday = InlineKeyboardButton(text='Понедельник', callback_data=f'teacher-Понедельник-{teacher}')
    tuesday = InlineKeyboardButton(text='Вторник', callback_data=f'teacher-Вторник-{teacher}')
    wednesday = InlineKeyboardButton(text='Среда', callback_data=f'teacher-Среда-{teacher}')
    thursday = InlineKeyboardButton(text='Четверг', callback_data=f'teacher-Четверг-{teacher}')
    friday = InlineKeyboardButton(text='Пятница', callback_data=f'teacher-Пятница-{teacher}')
    saturday = InlineKeyboardButton(text='Суббота', callback_data=f'teacher-Суббота-{teacher}')
    keyboard = InlineKeyboardBuilder().row(monday, thursday).row(tuesday, friday).row(wednesday, saturday).row(to_teacher).as_markup()
    return keyboard


def group_button(group: str) -> InlineKeyboardMarkup:
    """
    Make keyboard with "get schedule" button for provided teacher.
    :param group: Student's group
    :return: :class:`InlineKeyboardMarkup`: Keyboard with "get schedule" button for provided group
    """
    group = InlineKeyboardButton(text=group, callback_data=f'group_button-{group}')
    keyboard = InlineKeyboardBuilder().row(group).row(to_main).as_markup()
    return keyboard


def teacher_button(teacher: str) -> InlineKeyboardMarkup:
    """
    Make keyboard with "get teacher's schedule" button for provided teacher.
    :param teacher: Teacher's surname
    :return: :class:`InlineKeyboardMarkup`: Keyboard with "get teacher's schedule" button for provided teacher
    """
    teacher = InlineKeyboardButton(text=teacher, callback_data=f'teacher_button-{teacher}')
    keyboard = InlineKeyboardBuilder().row(teacher).row(to_main).as_markup()
    return keyboard


def student_week_kb(group: str) -> InlineKeyboardMarkup:
    """
    Make keyboard with weekdays buttons for provided group.
    :param group: Student's group
    :return: :class:`InlineKeyboardMarkup`: Keyboard with weekdays buttons for provided group
    """
    monday = InlineKeyboardButton(text='Понедельник', callback_data=f'student-Понедельник-{group}')
    tuesday = InlineKeyboardButton(text='Вторник', callback_data=f'student-Вторник-{group}')
    wednesday = InlineKeyboardButton(text='Среда', callback_data=f'student-Среда-{group}')
    thursday = InlineKeyboardButton(text='Четверг', callback_data=f'student-Четверг-{group}')
    friday = InlineKeyboardButton(text='Пятница', callback_data=f'student-Пятница-{group}')
    saturday = InlineKeyboardButton(text='Суббота', callback_data=f'student-Суббота-{group}')
    keyboard = InlineKeyboardBuilder().row(monday, thursday).row(tuesday, friday).row(wednesday, saturday).row(to_group).as_markup()
    return keyboard


def to_student_schedule_kb(group: str) -> InlineKeyboardMarkup:
    """
    Make keyboard with "return to weekday selection" button for provided group.
    :param group: Student's group
    :return: :class:`InlineKeyboardMarkup`: Keyboard with "return to weekday selection" button for provided group
    """
    student_schedule = InlineKeyboardButton(text='🔙 Назад', callback_data=f'group_button-{group}')
    keyboard = InlineKeyboardBuilder().row(student_schedule).as_markup()
    return keyboard


change_group = InlineKeyboardButton(text='🎒 Изменить класс', callback_data='change_group')
change_building = InlineKeyboardButton(text='🏫 Изменить корпус', callback_data='change_building')
change_teacher = InlineKeyboardButton(text='👩‍🏫 Изменить учителя', callback_data='change_teacher')
filled_profile_kb = InlineKeyboardBuilder().row(change_group).row(change_building).row(change_teacher).row(to_main).as_markup()

registration = InlineKeyboardButton(text='📝 Регистрация', callback_data='registration')
unfilled_profile_kb = InlineKeyboardBuilder().row(registration).row(to_main).as_markup()

building_1 = InlineKeyboardButton(text='1 корпус', callback_data='building-1')
building_2 = InlineKeyboardButton(text='2 корпус', callback_data='building-2')
building_3 = InlineKeyboardButton(text='3 корпус', callback_data='building-3')
building_4 = InlineKeyboardButton(text='4 корпус', callback_data='building-4')
buildings_kb = InlineKeyboardBuilder().row(building_1, building_2).row(building_3, building_4).row(to_main).as_markup()

food = InlineKeyboardButton(text='🍽 Питание', callback_data='food')
library = InlineKeyboardButton(text='📚 Библиотека', callback_data='library')
lessons = InlineKeyboardButton(text='🔔 Звонки', callback_data='lessons')
school_kb = InlineKeyboardBuilder().row(food).row(library).row(lessons).row(to_main).as_markup()

menu_1 = InlineKeyboardButton(text='Меню 1 корпуса', callback_data='menu-1')
menu_2 = InlineKeyboardButton(text='Меню 2 корпуса', callback_data='menu-2')
menu_3 = InlineKeyboardButton(text='Меню 3 корпуса', callback_data='menu-3')
food_kb = InlineKeyboardBuilder().row(menu_1).row(menu_2).row(menu_3).row(to_school).as_markup()

library_1 = InlineKeyboardButton(text='Библиотека 1 корпуса', callback_data='library_1')
library_2 = InlineKeyboardButton(text='Библиотека 2 корпуса', callback_data='library_2')
library_3 = InlineKeyboardButton(text='Библиотека 3 корпуса', callback_data='library_3')
library_kb = InlineKeyboardBuilder().row(library_1).row(library_2).row(library_3).row(to_school).as_markup()

news = InlineKeyboardButton(text='✉️ Рассылка', callback_data='news')
give_role = InlineKeyboardButton(text='👑 Выдать роль', callback_data='give_role')
newsman_kb = InlineKeyboardBuilder().row(news).row(to_main).as_markup()
admin_kb = InlineKeyboardBuilder().row(news).row(give_role).row(to_main).as_markup()

message_1 = InlineKeyboardButton(text='1 корпус', callback_data='message-1')
message_2 = InlineKeyboardButton(text='2 корпус', callback_data='message-2')
message_3 = InlineKeyboardButton(text='3 корпус', callback_data='message-3')
message_4 = InlineKeyboardButton(text='4 корпус', callback_data='message-4')
message_all = InlineKeyboardButton(text='Все корпуса', callback_data='message-all')
news_kb = InlineKeyboardBuilder().row(message_1, message_2).row(message_3, message_4).row(message_all).as_markup()

submit = InlineKeyboardButton(text='✅ Подтверждаю', callback_data='submit')
submit_kb = InlineKeyboardBuilder().row(submit).as_markup()

admin = InlineKeyboardButton(text='👨‍💻 Админ', callback_data='admin')
newsman = InlineKeyboardButton(text='👩‍💼 Новостник', callback_data='newsman')
roles_kb = InlineKeyboardBuilder().row(admin, newsman).as_markup()

approve_idea = InlineKeyboardButton(text='✅ Одобрить', callback_data='approve_idea')
idea_kb = InlineKeyboardBuilder().row(approve_idea).as_markup()


def bug_kb(tg: str) -> InlineKeyboardMarkup:
    fix_bug = InlineKeyboardButton(text='✅ Исправлено', callback_data=f'fix_bug-{tg}')
    reject_bug = InlineKeyboardButton(text='❌ Отклонить', callback_data=f'reject_bug-{tg}')
    keyboard = InlineKeyboardBuilder().row(fix_bug, reject_bug).as_markup()
    return keyboard
