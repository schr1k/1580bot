from aiogram.fsm.state import State, StatesGroup


class GetStudentSchedule(StatesGroup):
    """
    Represents the state group for getting student's schedule.
    """
    group = State()


class FindTeacher(StatesGroup):
    """
    Represents the state group for finding teacher's information.
    """
    teacher = State()


class News(StatesGroup):
    """
    Represents the state group for news submission and management.
    """
    message = State()
    target = State() 
    submit = State() 


class SuggestIdea(StatesGroup):
    """
    Represents the state group for suggesting ideas.
    """
    idea = State()


class ReportBug(StatesGroup):
    """
    Represents the state group for reporting bugs.
    """
    bug = State()


class Registration(StatesGroup):
    """
    Represents the state group for user registration.
    """
    building = State()
    group = State()
    teacher = State()


class ChangeGroup(StatesGroup):
    """
    Represents the state group for changing user's group.
    """
    group = State()


class ChangeBuilding(StatesGroup):
    """
    Represents the state group for changing user's building.
    """
    building = State()


class ChangeTeacher(StatesGroup):
    """
    Represents the state group for changing user's teacher.
    """
    teacher = State()


class GiveRole(StatesGroup):
    """
    Represents the state group for assigning roles to users.
    """
    id = State()
    role = State()
