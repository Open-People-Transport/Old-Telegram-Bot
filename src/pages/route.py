from uuid import UUID

import pygraphic
from pydantic import Field
from pygraphic import GQLParameters, GQLQuery, GQLType
from src.utils import request_query_parse_response
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from . import Page

pygraphic.types.register_graphql_type("UUID!", UUID)


class Parameters(GQLParameters):
    id: UUID


class Node(GQLType):
    id: UUID
    name: str


class Stop(GQLType):
    id: UUID
    lat: float
    lng: float
    node: Node


class RouteStop(GQLType):
    distance: int
    stop: Stop


class Route(GQLType):
    id: UUID
    number: str
    routeStops: list[RouteStop]


class GetRouteWithNodes(GQLQuery, parameters=Parameters):
    route: Route = Field(id=Parameters.id)


class RoutePage(Page):
    def __init__(self, route_id: str):
        result = request_query_parse_response(
            GetRouteWithNodes, Parameters(id=route_id)
        )

        self.message = f"Маршрут {result.route.number}"

        keyboard: list[list[InlineKeyboardButton]] = []
        COLUMNS = 1
        for i, route_stop in enumerate(result.route.routeStops):
            if not i % COLUMNS:
                keyboard.append([])
            button1 = InlineKeyboardButton(
                route_stop.stop.node.name, callback_data=f"stop {route_stop.stop.id}"
            )
            button2 = InlineKeyboardButton("?", callback_data="home")
            keyboard[-1].append(button1)
            keyboard[-1].append(button2)

        if not keyboard or len(keyboard[-1]) == COLUMNS + 1:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton("Назад", callback_data="routes"))

        self.keyboard = InlineKeyboardMarkup(keyboard)
