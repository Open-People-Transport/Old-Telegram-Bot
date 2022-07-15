from typing import Iterator
from uuid import UUID

from pygraphic import GQLQuery, GQLType
from src.utils import request_query_parse_response
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes


class Route(GQLType):
    id: UUID
    number: str


class GetAllRoutes(GQLQuery):
    routes: list[Route]


def get_message() -> tuple[str, InlineKeyboardMarkup]:
    data = request_query_parse_response(GetAllRoutes)

    text = f"Маршруты ({len(data.routes)})"

    def gen_keyboard() -> Iterator[list[InlineKeyboardButton]]:
        COLUMN_COUNT = 5
        for first_i in range(0, len(data.routes), COLUMN_COUNT):
            row = [
                InlineKeyboardButton("·", callback_data="blank")
                for _ in range(COLUMN_COUNT)
            ]
            for button, route in zip(row, data.routes[first_i:]):
                button.text = route.number.center(6)
                button.callback_data = f"route {route.id}"
            yield row
        yield [InlineKeyboardButton("Назад", callback_data="start")]

    return text, InlineKeyboardMarkup(list(gen_keyboard()))


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (query := update.callback_query) is not None
    text, reply_markup = get_message()
    await query.answer()
    await query.edit_message_text(text, reply_markup=reply_markup)


handler = CallbackQueryHandler(callback, "routes")
