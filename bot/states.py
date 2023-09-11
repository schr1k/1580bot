from aiogram.fsm.state import State, StatesGroup


class GetStudentSchedule(StatesGroup):
    group = State()
    weekday = State()


class GetTeacherSchedule(StatesGroup):
    teacher_surname = State()
    weekday = State()
