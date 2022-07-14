import logging

from telegram import Update
from telegram.ext import ContextTypes

from .decorators import callback_query_handler, command_handler, error_handler
from .exceptions import GeneralBotException
from .pages.home import HomePage
from .pages.route import RoutePage
from .pages.routes import RoutesPage


@command_handler("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        raise GeneralBotException
    page = HomePage()
    await update.message.reply_text(page.message, reply_markup=page.keyboard)


@command_handler("routes")
async def routes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        raise GeneralBotException
    page = RoutesPage()
    await update.message.reply_text(page.message, reply_markup=page.keyboard)


@command_handler("route")
async def route(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        raise GeneralBotException

    if context.args is None or len(context.args) != 1:
        raise ValueError("Wrong arguments")
    route_id = context.args[0]

    page = RoutePage(route_id)
    await update.message.reply_text(page.message, reply_markup=page.keyboard)


@callback_query_handler("home")
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (query := update.callback_query) is not None
    page = HomePage()
    await query.answer()
    await query.edit_message_text(page.message, reply_markup=page.keyboard)


@callback_query_handler("routes")
async def handle_routes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (query := update.callback_query) is not None
    page = RoutesPage()
    await query.answer()
    await query.edit_message_text(page.message, reply_markup=page.keyboard)


@callback_query_handler("route")
async def handle_route(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (query := update.callback_query) is not None
    assert query.data is not None
    args = query.data.split()[1:]
    assert len(args) == 1
    route_id = args[0]
    page = RoutePage(route_id)
    await query.answer()
    await query.edit_message_text(page.message, reply_markup=page.keyboard)


@error_handler()
async def error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (error := context.error) is not None
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
