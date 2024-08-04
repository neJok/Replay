from aiogram.fsm.state import StatesGroup, State

class QuotesState(StatesGroup):
    image = State()
    author = State()
    text = State()