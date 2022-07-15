from src.exceptions import GeneralBotException
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes


def get_message() -> tuple[str, InlineKeyboardMarkup]:
    text = "Open People Transport"
    keyboard = [
        [
            InlineKeyboardButton("Маршруты", callback_data="routes"),
        ]
    ]
    return text, InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        raise GeneralBotException
    text, reply_markup = get_message()
    await update.message.reply_text(text, reply_markup=reply_markup)


handler = CommandHandler("start", start)
