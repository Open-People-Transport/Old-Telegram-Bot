import html
import json
import logging
import traceback

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
