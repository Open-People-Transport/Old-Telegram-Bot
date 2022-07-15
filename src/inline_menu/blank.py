from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (query := update.callback_query) is not None
    await query.answer()


handler = CallbackQueryHandler(callback, "blank")
