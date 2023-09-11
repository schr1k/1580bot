from aiogram.fsm.state import State, StatesGroup


class GetSchedule(StatesGroup):
    group = State()


class GetTeachersSchedule(StatesGroup):
    teachers_name = State()
    weekday = State()
