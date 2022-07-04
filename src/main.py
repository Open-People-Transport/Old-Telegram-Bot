import logging

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

    application.run_polling()
