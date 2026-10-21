import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ChatJoinRequest

from bot.config import config
from bot.keyboards import (
    cancel_keyboard,
    info_keyboard,
    join_request_keyboard,
    main_keyboard,
    url_keyboard,
    welcome_inline_keyboard,
)
from bot.texts import INFO_MENU, WAITING_INFO, MESSAGE_SENT, CANCELLED, welcome

router = Router()


class InfoState(StatesGroup):
    waiting_message = State()


class ReplyState(StatesGroup):
    waiting_reply = State()


async def show_home(message: Message):
    name = message.from_user.first_name or "друг"
    await message.answer(
        welcome(name, config.bot_name),
        reply_markup=welcome_inline_keyboard(),
    )


async def open_chat(message: Message):
    if not config.chat_url:
        await message.answer("⚠️ Ссылка на чат не настроена.", reply_markup=main_keyboard())
        return
    await message.answer(
        "💬 Перейти в чат:",
        reply_markup=url_keyboard(config.chat_url, "💬 Открыть чат"),
    )


async def open_support(message: Message):
    if not config.support_url:
        await message.answer("⚠️ Ссылка на поддержку не настроена.", reply_markup=main_keyboard())
        return
    await message.answer(
        "❤️ Поддержать проект:",
        reply_markup=url_keyboard(config.support_url, "❤️ Поддержать"),
    )


async def open_info(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(INFO_MENU, reply_markup=info_keyboard())


async def go_home(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню:", reply_markup=main_keyboard())


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, bot: Bot):
    await state.clear()

    user = message.from_user

    for admin_id in config.admin_ids:
        try:
            text = (
                "🔔 <b>Пользователь запустил бота</b>\n\n"
                f"👤 <b>Имя:</b> {user.full_name}\n"
                f"🆔 <b>Telegram ID:</b> <code>{user.id}</code>\n"
                f"🔗 <b>Username:</b> @{user.username if user.username else 'не указан'}\n"
                f"🌐 <b>Язык:</b> {user.language_code or 'не указан'}\n"
                f"⭐ <b>Telegram Premium:</b> {'Да' if user.is_premium else 'Нет'}"
            )

            await bot.send_message(admin_id, text)

        except Exception:
            logging.exception(
                "Не удалось отправить уведомление администратору %s",
                admin_id,
            )

    await show_home(message)
   

@router.message(F.text == "💬 Перейти в чат единомышленников")
async def chat_button(message: Message):
    await open_chat(message)


@router.message(F.text == "❤️ Поддержать проекты")
async def support_button(message: Message):
    await open_support(message)


@router.message(F.text == "📩 Сообщить информацию")
async def info_button(message: Message, state: FSMContext):
    await open_info(message, state)


@router.message(F.text == "📍 Сообщить координаты 'важных' мест")
async def places_button(message: Message, state: FSMContext):
    await state.update_data(info_type="Сообщить о местах")
    await state.set_state(InfoState.waiting_message)
    await message.answer(
        "📍 <b>Сообщить координаты 'важных' мест</b>\n\n" + WAITING_INFO,
        reply_markup=cancel_keyboard(),
    )


@router.message(F.text == "📄 Оставить резюме для вступления в ряды добровольцев")
async def resume_button(message: Message, state: FSMContext):
    await state.update_data(info_type="Оставить резюме для вступления в ряды бойцов")
    await state.set_state(InfoState.waiting_message)
    await message.answer(
        "📄 <b>Оставить резюме для вступления в ряды добровольцев</b>\n\n" + WAITING_INFO,
        reply_markup=cancel_keyboard(),
    )

@router.message(F.text == "📄 Прислать интересные кадры (прилеты, объекты и т.д.)")
async def resume_button(message: Message, state: FSMContext):
    await state.update_data(info_type="Прислать интересное видео")
    await state.set_state(InfoState.waiting_message)
    await message.answer(
        "📄 <b>Прислать интересные кадры (прилеты, объекты и т.д.)</b>\n\n" + WAITING_INFO,
        reply_markup=cancel_keyboard(),
    )

@router.message(F.text == "📄 Предоставить данные 'важных' людей")
async def resume_button(message: Message, state: FSMContext):
    await state.update_data(info_type="Сообщить о наболевшем")
    await state.set_state(InfoState.waiting_message)
    await message.answer(
        "📄 <b>Предоставить данные 'важных' людей</b>\n\n" + WAITING_INFO,
        reply_markup=cancel_keyboard(),
    )

@router.message(F.text == "📄 Сообщить другую информацию")
async def resume_button(message: Message, state: FSMContext):
    await state.update_data(info_type="Сообщить о наболевшем")
    await state.set_state(InfoState.waiting_message)
    await message.answer(
        "📄 <b>Сообщить другую информацию</b>\n\n" + WAITING_INFO,
        reply_markup=cancel_keyboard(),
    )

@router.message(F.text == "↩️ Назад")
async def back_button(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == InfoState.waiting_message.state:
        await open_info(message, state)
        return
    await go_home(message, state)


@router.message(InfoState.waiting_message)
async def user_information(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    info_type = data.get("info_type", "Информация")
    user = message.from_user

    header = (
        "📩 <b>Новая информация от пользователя</b>\n\n"
        f"📌 <b>Тип:</b> {info_type}\n"
        f"👤 <b>Имя:</b> {user.full_name}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
    )
    if user.username:
        header += f"🔗 <b>Username:</b> @{user.username}\n"
    header += "\n"

    sent = False
    for admin_id in config.admin_ids:
        try:
            if message.text:
                await bot.send_message(
                    admin_id,
                    header + f"💬 <b>Сообщение:</b>\n{message.text}",
                )
            else:
                await bot.send_message(admin_id, header + "💬 Пользователь отправил вложение:")
                await bot.copy_message(admin_id, message.chat.id, message.message_id)
            await bot.send_message(
                admin_id,
                "↩️ Ответить пользователю можно командой:\n"
                f"<code>/reply {user.id}</code>",
            )
            sent = True
        except Exception:
            logging.exception("Не удалось отправить информацию администратору %s", admin_id)

    if sent:
        await message.answer(MESSAGE_SENT, reply_markup=main_keyboard())
    else:
        await message.answer(
            "⚠️ Не удалось отправить информацию администратору. Попробуйте позже.",
            reply_markup=main_keyboard(),
        )
    await state.clear()


@router.callback_query(F.data == "home_chat")
async def home_chat_callback(callback: CallbackQuery):
    await open_chat(callback.message)
    await callback.answer()


@router.callback_query(F.data == "home_support")
async def home_support_callback(callback: CallbackQuery):
    await open_support(callback.message)
    await callback.answer()


@router.callback_query(F.data == "home_info")
async def home_info_callback(callback: CallbackQuery, state: FSMContext):
    await open_info(callback.message, state)
    await callback.answer()


@router.message(Command("reply"))
async def reply_command(message: Message, state: FSMContext):
    if message.from_user.id not in config.admin_ids:
        await message.answer("⛔ У вас нет доступа к этой команде.")
        return
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Использование:\n<code>/reply USER_ID</code>")
        return
    user_id = int(parts[1])
    await state.update_data(reply_user_id=user_id)
    await state.set_state(ReplyState.waiting_reply)
    await message.answer(
        f"✍️ Напишите ответ пользователю <code>{user_id}</code>.",
        reply_markup=cancel_keyboard(),
    )


@router.message(ReplyState.waiting_reply)
async def send_admin_reply(message: Message, state: FSMContext, bot: Bot):
    if message.from_user.id not in config.admin_ids:
        await state.clear()
        return
    data = await state.get_data()
    user_id = data.get("reply_user_id")
    if not user_id:
        await state.clear()
        await message.answer("⚠️ Пользователь не найден.")
        return
    try:
        if message.text:
            await bot.send_message(
                user_id,
                "👨‍💼 <b>Ответ администратора:</b>\n\n" + message.text,
            )
        else:
            await bot.send_message(user_id, "👨‍💼 Администратор отправил сообщение:")
            await bot.copy_message(user_id, message.chat.id, message.message_id)
        await message.answer("✅ Ответ отправлен пользователю.", reply_markup=main_keyboard())
    except Exception:
        await message.answer("⚠️ Не удалось отправить сообщение пользователю.")
    await state.clear()
 
@router.chat_join_request()
async def join_request_handler(request: ChatJoinRequest, bot: Bot):
    user = request.from_user
    chat_title = request.chat.title or str(request.chat.id)
    text = (
        "🔔 <b>Новая заявка на вступление</b>\n\n"
        f"👤 <b>Имя:</b> {user.full_name}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
    )
    if user.username:
        text += f"🔗 <b>Username:</b> @{user.username}\n"
    text += f"💬 <b>Чат:</b> {chat_title}"

    keyboard = join_request_keyboard(request.chat.id, user.id)
    for admin_id in config.admin_ids:
        try:
            await bot.send_message(admin_id, text, reply_markup=keyboard)
        except Exception:
            logging.exception("Не удалось отправить заявку администратору %s", admin_id)


@router.callback_query(F.data.startswith("join:"))
async def join_request_action(callback: CallbackQuery, bot: Bot):
    if callback.from_user.id not in config.admin_ids:
        await callback.answer("⛔ У вас нет доступа.", show_alert=True)
        return

    parts = (callback.data or "").split(":")
    if len(parts) != 4:
        await callback.answer("Некорректная заявка.", show_alert=True)
        return

    action = parts[1]
    try:
        chat_id = int(parts[2])
        user_id = int(parts[3])
    except ValueError:
        await callback.answer("Некорректные данные.", show_alert=True)
        return

    try:
        if action == "approve":
            await bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
            result = "✅ Заявка одобрена."
        elif action == "decline":
            await bot.decline_chat_join_request(chat_id=chat_id, user_id=user_id)
            result = "❌ Заявка отклонена."
        else:
            await callback.answer("Неизвестное действие.", show_alert=True)
            return

        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(result)
        await callback.answer(result)
    except Exception:
        logging.exception("Ошибка обработки заявки")
        await callback.answer(
            "⚠️ Не удалось обработать заявку. Проверьте права бота.",
            show_alert=True,
        )


async def run_bot():
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)
    logging.info("Бот запускается...")
    await dp.start_polling(bot)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    try:
        asyncio.run(run_bot())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
