from src.exceptions import GeneralBotException
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def route(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        raise GeneralBotException

    if context.args is None or len(context.args) != 1:
        raise ValueError("Wrong arguments")

    raise NotImplementedError
    await update.message.reply_text(text)


handler = CommandHandler("route", route)
