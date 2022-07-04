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
                f"{route.number: ^10}", callback_data=f"route {route.id}"
            )
            keyboard[-1].append(button)

        keyboard[-1].extend(
            [InlineKeyboardButton(" ", callback_data="routes")]
            * (COLUMNS - len(keyboard[-1]))
        )
        keyboard.append([InlineKeyboardButton("Назад", callback_data="home")])

        self.keyboard = InlineKeyboardMarkup(keyboard)
