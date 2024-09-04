from aiogram.fsm.state import StatesGroup, State

class NewsState(StatesGroup):
    image = State()
    text = State()