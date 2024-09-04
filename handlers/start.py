import config
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards import kb_menu
from states import AuthState

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if await config.db.users.count_documents({"_id": message.from_user.id}) == 0:
        await state.set_state(AuthState.password)
        return await message.answer("Введите пароль от бота:", reply_markup=ReplyKeyboardRemove())

    await message.answer('Что будем генерировать?', reply_markup=kb_menu)

@start_router.message(
    F.text == '🛑 Назад'
)
async def back(message: Message, state: FSMContext):
    await state.clear()
    await cmd_start(message, state)