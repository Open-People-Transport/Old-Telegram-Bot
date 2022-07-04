from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from . import Page


class HomePage(Page):
    def __init__(self):
        self.message = f"Open People Tranport"
        self.keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Маршруты", callback_data="routes"),
                ]
            ]
        )
