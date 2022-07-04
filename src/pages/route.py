from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .. import db
from . import Page


class RoutePage(Page):
    def __init__(self, route_id: str):
        route = db.get_route(route_id)
        self.message = f"Маршрут {route.number}"

        keyboard = []
        COLUMNS = 1
        for i, stop in enumerate(route.stops):
            if not i % COLUMNS:
                keyboard.append([])
            button1 = InlineKeyboardButton(stop.name, callback_data=f"stop {stop.id}")
            button2 = InlineKeyboardButton(stop.time, callback_data="home")
            keyboard[-1].append(button1)
            keyboard[-1].append(button2)

        if len(keyboard[-1]) == COLUMNS + 1:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton("Назад", callback_data="routes"))

        self.keyboard = InlineKeyboardMarkup(keyboard)
