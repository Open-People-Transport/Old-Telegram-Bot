import logging

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes


async def error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (error := context.error) is not None

    if type(error) is BadRequest and error.message.startswith(
        "Message is not modified"
    ):
        return

    logging.exception(error)

    assert isinstance(update, Update)

    answer = error.__class__.__name__

    if update.callback_query:
        MAX_LENGTH = 200
        await update.callback_query.answer(answer[:MAX_LENGTH], show_alert=False)
    else:
        MAX_LENGTH = 4096
        assert update.effective_message is not None
        await update.effective_message.reply_text(answer[:MAX_LENGTH])
