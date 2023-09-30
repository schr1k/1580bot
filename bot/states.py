from aiogram.fsm.state import State, StatesGroup


class GetStudentSchedule(StatesGroup):
    group = State()
    weekday = State()


class GetTeacherSchedule(StatesGroup):
    teacher_surname = State()
    weekday = State()


class News(StatesGroup):
    message = State()
    target = State()
    submit = State()


class SuggestIdea(StatesGroup):
    idea = State()


class Registration(StatesGroup):
    building = State()
    group = State()


class ChangeGroup(StatesGroup):
    group = State()


class ChangeBuilding(StatesGroup):
    building = State()


class GiveRole(StatesGroup):
    id = State()
    role = State()

