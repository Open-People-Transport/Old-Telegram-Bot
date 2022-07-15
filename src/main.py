import logging

from telegram.ext import ApplicationBuilder

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

application = ApplicationBuilder().token(BOT_TOKEN).build()
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
