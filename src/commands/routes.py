from src.exceptions import GeneralBotException
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        raise GeneralBotException
    raise NotImplementedError
    await update.message.reply_text(text)


handler = CommandHandler("routes", callback)
