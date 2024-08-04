from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import kb_menu

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Что будем генерировать?', reply_markup=kb_menu)

@start_router.message(
    F.text == '🛑 Назад'
)
async def back(message: Message, state: FSMContext):
    await state.clear()
    await cmd_start(message)