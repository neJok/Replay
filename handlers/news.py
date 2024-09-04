import config

from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, BufferedInputFile
from aiogram.fsm.context import FSMContext

from states import NewsState, AuthState
from draw import news as news_draw
from keyboards import kb_back
from .start import cmd_start

news_router = Router()

@news_router.message(F.text == '🗞️ Новость')
async def news(message: Message, state: FSMContext):
    if await config.db.users.count_documents({"_id": message.from_user.id}) == 0:
        await state.set_state(AuthState.password)
        return await message.answer("Введите пароль от бота:", reply_markup=ReplyKeyboardRemove())
    
    await message.answer('Отправьте фото для новости', reply_markup=kb_back)
    await state.set_state(NewsState.image)


@news_router.message(
    NewsState.image, 
    F.document
)
async def news_image(message: Message, state: FSMContext):
    await state.update_data(image=message.document.file_id)
    await message.answer(
        text="Отправьте текст новости",
    )
    await state.set_state(NewsState.text)

@news_router.message(
    NewsState.image, 
    F.photo
)
async def news_image_error(message: Message):
    await message.answer(
        text="Извините, но чтобы загрузить фотографию, пришлите её как файл!",
    )


@news_router.message(
    NewsState.text, 
    F.text
)
async def news_text(message: Message, state: FSMContext, bot: Bot):
    msg = await message.answer(
        text="Генерация...",
        reply_markup=ReplyKeyboardRemove()
    )

    data = await state.get_data()
    file = await news_draw.get_img({
        "image": await bot.download(data['image']),
        "text": message.text,
    })

    await message.answer_photo(BufferedInputFile(file.read(), filename='news.png'))
    await msg.delete()
    await state.clear()
    await cmd_start(message, state)
