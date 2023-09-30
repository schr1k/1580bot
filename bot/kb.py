from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import config

# Назад ================================================================================================================
to_main = InlineKeyboardButton(text='🔙 На Главную', callback_data='to_main')
to_main_kb = InlineKeyboardBuilder().add(to_main).as_markup()

to_admin_panel = InlineKeyboardButton(text='🔙 Админ-панель', callback_data='admin_panel')
to_admin_panel_kb = InlineKeyboardBuilder().add(to_admin_panel).as_markup()


# Главная ==============================================================================================================
get_schedule = InlineKeyboardButton(text='🗓 Получить расписание', callback_data='get_student_schedule')
find_teacher = InlineKeyboardButton(text='🔍 Найти учителя', callback_data='get_teacher_schedule')
suggest_idea = InlineKeyboardButton(text='💡 Предложить идею', callback_data='suggest_idea')
profile = InlineKeyboardButton(text='👤 Профиль', callback_data='profile')
user_main_kb = InlineKeyboardBuilder().row(get_schedule).row(find_teacher).row(suggest_idea).row(profile).as_markup()

admin_panel = InlineKeyboardButton(text='👨‍💻 Админ панель', callback_data='admin_panel')
staff_main_kb = InlineKeyboardBuilder().row(get_schedule).row(find_teacher).row(suggest_idea).row(profile).row(admin_panel).as_markup()


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


# Профиль (заполненный) ================================================================================================
change_group = InlineKeyboardButton(text='🎒 Изменить класс', callback_data='change_group')
change_building = InlineKeyboardButton(text='🏫 Изменить корпус', callback_data='change_building')
filled_profile_kb = InlineKeyboardBuilder().row(change_group).row(change_building).row(to_main).as_markup()


# Профиль (незаполненный) ==============================================================================================
registration = InlineKeyboardButton(text='📝 Регистрация', callback_data='registration')
unfilled_profile_kb = InlineKeyboardBuilder().row(registration).row(to_main).as_markup()


# Корпуса ==============================================================================================================
building_1 = InlineKeyboardButton(text='1 корпус', callback_data='building-1')
building_2 = InlineKeyboardButton(text='2 корпус', callback_data='building-2')
building_3 = InlineKeyboardButton(text='3 корпус', callback_data='building-3')
building_4 = InlineKeyboardButton(text='4 корпус', callback_data='building-4')
buildings_kb = InlineKeyboardBuilder().row(building_1, building_2).row(building_3, building_4).row(to_main).as_markup()


# Админ панель =========================================================================================================
news = InlineKeyboardButton(text='✉️ Рассылка', callback_data='news')
give_role = InlineKeyboardButton(text='👑 Выдать роль', callback_data='give_role')
newsman_kb = InlineKeyboardBuilder().row(news).row(to_main).as_markup()
admin_kb = InlineKeyboardBuilder().row(news).row(give_role).row(to_main).as_markup()


# Рассылка =============================================================================================================
message_1 = InlineKeyboardButton(text='1 корпус', callback_data='message-1')
message_2 = InlineKeyboardButton(text='2 корпус', callback_data='message-2')
message_3 = InlineKeyboardButton(text='3 корпус', callback_data='message-3')
message_4 = InlineKeyboardButton(text='4 корпус', callback_data='message-4')
message_all = InlineKeyboardButton(text='Все корпуса', callback_data='message-all')
news_kb = InlineKeyboardBuilder().row(message_1, message_2).row(message_3, message_4).row(message_all).as_markup()


# Подтверждение рассылки ===============================================================================================
submit = InlineKeyboardButton(text='✅ Подтверждаю', callback_data='submit')
submit_kb = InlineKeyboardBuilder().row(submit).as_markup()


# Выдача роли ==========================================================================================================
admin = InlineKeyboardButton(text='👨‍💻 Админ', callback_data='admin')
newsman = InlineKeyboardButton(text='👩‍🏫👩‍💼 Новостник', callback_data='newsman')
roles_kb = InlineKeyboardBuilder().row(admin, newsman).as_markup()

