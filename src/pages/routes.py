from uuid import UUID

from pygraphic import GQLQuery, GQLType
from src.utils import request_query_parse_response
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from . import Page


class Route(GQLType):
    id: UUID
    number: str


class GetAllRoutes(GQLQuery):
    routes: list[Route]


class RoutesPage(Page):
    def __init__(self):
        result = request_query_parse_response(GetAllRoutes)

        self.message = f"Маршруты ({len(result.routes)})"

        keyboard = []
        COLUMNS = 5
        for i, route in enumerate(result.routes):
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
