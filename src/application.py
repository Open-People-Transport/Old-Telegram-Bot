import logging

from telegram.ext import ApplicationBuilder

from .secret import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

application = ApplicationBuilder().token(BOT_TOKEN).build()


def run():
    application.run_polling()
