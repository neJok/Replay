from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📰 Цитату"),
        ],
    ],
    resize_keyboard=True,
)

kb_back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛑 Назад"),
        ],
    ],
    resize_keyboard=True,
)
