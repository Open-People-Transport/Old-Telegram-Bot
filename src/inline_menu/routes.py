from typing import Iterator
from uuid import UUID

from pydantic import Field
from pygraphic import GQLParameters, GQLQuery, GQLType
from src.utils import get_unique_blank, request_query_parse_response
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes


class Parameters(GQLParameters):
    type_name: str


class Route(GQLType):
    id: UUID
    number: str


class Type(GQLType):
    name: str
    routes: list[Route]


class EmptyType(GQLType):
    name: str


class GetRoutesForType(GQLQuery, parameters=Parameters):
    type: Type = Field(name=Parameters.type_name)
    types: list[EmptyType]


def translate_routes_title(count: int = 10):
    if not 10 <= count % 100 <= 20:
        if count % 10 == 1:
            return f"{count} маршрут"
        if count % 10 in (2, 3, 4):
            return f"{count} маршрута"
    return f"{count or 'нет'} маршрутов"


def translate_title_type_name(type_name: str):
    match type_name:
        case "bus":
            return "автобуса"
        case "trolley":
            return "троллейбуса"
        case "tram":
            return "трамвая"
        case "train":
            return "поезда"
    return f"({type_name})"


def translate_type_name(type_name: str):
    match type_name:
        case "bus":
            return "автобус"
        case "trolley":
            return "троллейбус"
        case "tram":
            return "трамвай"
        case "train":
            return "поезд"
    return f"({type_name})"


def get_message(selected_type: str = "bus") -> tuple[str, InlineKeyboardMarkup]:
    data = request_query_parse_response(
        GetRoutesForType, Parameters(type_name=selected_type)
    )

    title = translate_routes_title(len(data.type.routes)).capitalize()
    title_type_name = translate_title_type_name(data.type.name)
    text = f"{title} {title_type_name}"

    def gen_keyboard() -> Iterator[list[InlineKeyboardButton]]:
        COLUMN_COUNT = 5
        for first_i in range(0, len(data.type.routes), COLUMN_COUNT):
            row = [
                InlineKeyboardButton("·", callback_data=get_unique_blank())
                for _ in range(COLUMN_COUNT)
            ]
            for button, route in zip(row, data.type.routes[first_i:]):
                button.text = route.number.center(6)
                button.callback_data = f"route {route.id}"
            yield row

        COLUMN_COUNT = 2
        for first_i in range(0, len(data.types), COLUMN_COUNT):

            def gen_buttons():
                for type in data.types[first_i : first_i + COLUMN_COUNT]:
                    type_name = translate_type_name(type.name).capitalize()
                    if type.name == selected_type:
                        type_name = f"💠 {type_name} 💠"
                    yield InlineKeyboardButton(
                        type_name, callback_data=f"routes {type.name}"
                    )

            yield list(gen_buttons())
        yield [InlineKeyboardButton("Назад", callback_data="start")]

    return text, InlineKeyboardMarkup(list(gen_keyboard()))


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert (query := update.callback_query) is not None
    assert query.data is not None
    args = query.data.split()[1:]
    text, reply_markup = get_message(*args)
    await query.answer()
    await query.edit_message_text(text, reply_markup=reply_markup)


handler = CallbackQueryHandler(callback, "routes")
