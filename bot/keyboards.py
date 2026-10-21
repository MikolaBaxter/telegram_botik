from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💬 Перейти в чат единомышленников")],
            [KeyboardButton(text="❤️ Поддержать проекты"), KeyboardButton(text="📩 Сообщить информацию")],
        ],
        resize_keyboard=True,
        is_persistent=False,
        input_field_placeholder="Выберите действие…",
    )


def info_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Сообщить координаты 'важных' мест")],
            [KeyboardButton(text="📄 Оставить резюме для вступления в ряды добровольцев")],
            [KeyboardButton(text="📄 Прислать интересные кадры (прилеты, объекты и т.д.)")],
            [KeyboardButton(text="📄 Предоставить данные 'важных' людей")],
            [KeyboardButton(text="📄 Сообщить другую информацию")],
            [KeyboardButton(text="↩️ Назад")],
        ],
        resize_keyboard=True,
        is_persistent=False,
        input_field_placeholder="Выберите действие…",
    )


def cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="↩️ Назад")]],
        resize_keyboard=True,
        is_persistent=False,
        input_field_placeholder="Введите сообщение…",
    )


def url_keyboard(url: str, text: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=text, url=url)]]
    )


def welcome_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Перейти в чат единомышленников", callback_data="home_chat")],
            [InlineKeyboardButton(text="❤️ Поддержать проекты", callback_data="home_support")],
            [InlineKeyboardButton(text="📩 Сообщить информацию", callback_data="home_info")],
        ]
    )


def join_request_keyboard(chat_id: int, user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"join:approve:{chat_id}:{user_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"join:decline:{chat_id}:{user_id}"),
        ]]
    )
