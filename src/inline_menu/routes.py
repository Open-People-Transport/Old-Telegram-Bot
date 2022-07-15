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

    keyboard: list[list[InlineKeyboardButton]] = []
    COLUMNS = 5
    for i, route in enumerate(data.routes):
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
    keyboard.append([InlineKeyboardButton("Назад", callback_data="start")])

    return text, InlineKeyboardMarkup(keyboard)


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (query := update.callback_query) is not None
    text, reply_markup = get_message()
    await query.answer()
    await query.edit_message_text(text, reply_markup=reply_markup)


handler = CallbackQueryHandler(callback, "routes")
