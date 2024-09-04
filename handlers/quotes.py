import config

from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, BufferedInputFile
from aiogram.fsm.context import FSMContext

from states import QuotesState, AuthState
from draw import quotes as quotes_draw
from keyboards import kb_back
from .start import cmd_start

quotes_router = Router()

@quotes_router.message(F.text == '📰 Цитату')
async def quotes(message: Message, state: FSMContext):
    if await config.db.users.count_documents({"_id": message.from_user.id}) == 0:
        await state.set_state(AuthState.password)
        return await message.answer("Введите пароль от бота:", reply_markup=ReplyKeyboardRemove())
    
    await message.answer('Отправьте фото для цитаты', reply_markup=kb_back)
    await state.set_state(QuotesState.image)


@quotes_router.message(
    QuotesState.image, 
    F.document
)
async def quotes_image(message: Message, state: FSMContext):
    await state.update_data(image=message.document.file_id)
    await message.answer(
        text="Отправьте автора цитаты",
    )
    await state.set_state(QuotesState.author)

@quotes_router.message(
    QuotesState.image, 
    F.photo
)
async def quotes_image_error(message: Message):
    await message.answer(
        text="Извините, но чтобы загрузить фотографию, пришлите её как файл!",
    )

@quotes_router.message(
    QuotesState.author, 
    F.text
)
async def quotes_author(message: Message, state: FSMContext):
    await state.update_data(author=message.text)
    await message.answer(
        text="Отправьте текст цитаты",
    )
    await state.set_state(QuotesState.text)


@quotes_router.message(
    QuotesState.text, 
    F.text
)
async def quotes_text(message: Message, state: FSMContext, bot: Bot):
    msg = await message.answer(
        text="Генерация...",
        reply_markup=ReplyKeyboardRemove()
    )

    data = await state.get_data()
    file = await quotes_draw.get_img({
        "image": await bot.download(data['image']),
        "author": data['author'],
        "text": message.text,
    })

    await message.answer_photo(BufferedInputFile(file.read(), filename='quote.png'))
    await msg.delete()
    await state.clear()
    await cmd_start(message, state)
