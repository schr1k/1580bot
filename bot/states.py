from aiogram.fsm.state import State, StatesGroup


class GetSchedule(StatesGroup):
    group = State()
