from aiogram.fsm.state import StatesGroup, State

class AuthState(StatesGroup):
    password = State()
    
class ChangePasswordState(StatesGroup):
    new_password = State()