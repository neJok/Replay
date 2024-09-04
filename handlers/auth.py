import config

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from states import AuthState, ChangePasswordState
from keyboards import kb_back, kb_menu

auth_router = Router()

@auth_router.message(
    AuthState.password,
    F.text
)
async def quotes_image(message: Message, state: FSMContext):
    entry = await config.db.config.find_one({"_id": "password"})
    if message.text != entry['password']:
        return await message.answer('Неправильный пароль, попробуйте еще раз:')

    await state.clear()
    await config.db.users.insert_one({"_id": message.from_user.id})

    await message.answer(
        text="Правильный пароль, что будем генерировать?",
        reply_markup=kb_menu
    )

@auth_router.message(Command("password"))
async def change_password(message: Message, state: FSMContext):
    if message.from_user.id not in config.ADMINS:
        return 
    
    await message.answer('Введите новый пароль:', reply_markup=kb_back)
    await state.set_state(ChangePasswordState.new_password)

@auth_router.message(
    ChangePasswordState.new_password,
    F.text
)
async def new_password(message: Message, state: FSMContext):
    await state.clear()
    
    await config.db.config.update_one({"_id": "password"}, {"$set": {"password": message.text}})
    await config.db.users.delete_many({"_id": {"$nin": config.ADMINS}})

    await message.answer(
        text="Новый пароль поставлен, что будем генерировать?",
        reply_markup=kb_menu
    )