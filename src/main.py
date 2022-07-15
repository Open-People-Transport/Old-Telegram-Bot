import logging

from telegram import Bot, BotCommand
from telegram.ext import Application, ApplicationBuilder

import src.commands.route
import src.commands.routes
import src.commands.start
import src.handlers
import src.inline_menu.route
import src.inline_menu.routes
import src.inline_menu.start

from .secret import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def post_init(application: Application):
    bot: Bot = application.bot
    await bot.set_my_commands(
        [
            BotCommand("start", "Display the starting menu"),
            BotCommand("routes", "Display information about all transport routes"),
            BotCommand("route", "Display information about a specific transport route"),
            BotCommand("help", "Display the help menu"),
        ]
    )


application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
application.add_handlers(
    [
        src.commands.start.handler,
        src.commands.routes.handler,
        src.commands.route.handler,
        src.inline_menu.start.handler,
        src.inline_menu.routes.handler,
        src.inline_menu.route.handler,
    ]
)
application.add_error_handler(src.handlers.error)


def run():
    application.run_polling()


if __name__ == "__main__":
    run()
