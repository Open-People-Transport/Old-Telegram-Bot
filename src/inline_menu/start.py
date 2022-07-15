from src.commands.start import get_message
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (query := update.callback_query) is not None
    text, reply_markup = get_message()
    await query.answer()
    await query.edit_message_text(text, reply_markup=reply_markup)


handler = CallbackQueryHandler(callback, "start")
