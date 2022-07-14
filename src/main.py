import html
import json
import logging
import traceback

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from .pages.home import HomePage
from .pages.route import RoutePage
from .pages.routes import RoutesPage
from .secret import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    page = HomePage()
    if query := update.callback_query:
        await query.answer()
        await query.edit_message_text(page.message, reply_markup=page.keyboard)
    elif message := update.message:
        await message.reply_text(page.message, reply_markup=page.keyboard)
    else:
        raise RuntimeError("Unknown update type")


async def handle_routes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    page = RoutesPage()
    if query := update.callback_query:
        await query.answer()
        await query.edit_message_text(page.message, reply_markup=page.keyboard)
    elif message := update.message:
        await message.reply_text(page.message, reply_markup=page.keyboard)
    else:
        raise RuntimeError("Unknown update type")


async def handle_route(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if query := update.callback_query:
        page = RoutePage(query.data.split(maxsplit=1)[1])
        await query.answer()
        await query.edit_message_text(page.message, reply_markup=page.keyboard)
    elif message := update.message:
        page = RoutePage("unknown")
        await message.reply_text(page.message, reply_markup=page.keyboard)
    else:
        raise RuntimeError("Unknown update type")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert context.error is not None

    logging.exception(context.error)

    assert isinstance(update, Update)
    tb_list = traceback.format_exception(context.error)
    tb_string = "".join(tb_list)

    update_str = update.to_dict()
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
    )

    left_length = 4096 - len(message) - len("<pre></pre>")

    message_tb_part = html.escape(tb_string)[:left_length]

    message += f"<pre>{message_tb_part}</pre>"

    assert update.effective_message is not None
    await update.effective_message.reply_text(message, parse_mode="HTML")


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handlers(
        [
            CommandHandler("start", handle_start),
            CommandHandler("routes", handle_routes),
            CommandHandler("route", handle_route),
            CallbackQueryHandler(handle_start, pattern="home"),
            CallbackQueryHandler(handle_routes, pattern="routes"),
            CallbackQueryHandler(handle_route, pattern="route .+"),
        ]
    )
    application.add_error_handler(error_handler)

    application.run_polling()
