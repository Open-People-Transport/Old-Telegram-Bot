from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .. import db
from . import Page


class RoutesPage(Page):
    def __init__(self):
        self.message = f"Маршруты ({len(db.routes)})"

        keyboard = []
        COLUMNS = 5
        for i, route in enumerate(db.routes):
            if not i % COLUMNS:
                keyboard.append([])
            button = InlineKeyboardButton(
                route.number, callback_data=f"route {route.id}"
            )
            keyboard[-1].append(button)

        if len(keyboard[-1]) == COLUMNS:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton("Назад", callback_data="home"))

        self.keyboard = InlineKeyboardMarkup(keyboard)
