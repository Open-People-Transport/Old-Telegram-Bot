from dataclasses import dataclass
from random import choices, randint
from string import ascii_letters, digits
from typing import Optional
from uuid import UUID, uuid4


def randword():
    return "".join(choices(ascii_letters, k=randint(12, 18)))


@dataclass
class Route:
    id: UUID
    number: str
    stops: list["Stop"]

    def __lt__(self, other):
        return len(self.number) < len(other.number) or self.number < other.number


@dataclass
class Stop:
    id: UUID
    name: str
    wait_down: int = 0
    wait_up: int = 0
    bus_down: Optional[str] = None
    bus_up: Optional[str] = None

    @property
    def time(self):
        bus_down = self.bus_down or "–––"
        bus_up = self.bus_up or "–––"
        return (
            f"{bus_down}  ↓  {self.wait_down: >2}  |  {self.wait_up: >2}  ↑  {bus_up}"
        )


routes: list[Route] = []
for i in range(60):
    number = str(randint(1, 99))
    if i == 0:
        number = str(41)
    if any(map(lambda route: route.number == number, routes)):
        continue
    stops: list[Stop] = []
    for _ in range(randint(20, 30)):
        prev_down = stops[-1].wait_down if stops else 0
        prev_up = stops[-1].wait_up if stops else 0

        if delta_up := randint(0, 6):
            up = prev_up + delta_up
            bus_up = None
        else:
            up = 0
            bus_up = "".join(choices(digits, k=3))

        if (delta_down := randint(1, 6)) > prev_down:
            down = randint(15, 60)
            if stops:
                stops[-1].bus_down = "".join(choices(digits, k=3))
        else:
            down = prev_down - delta_down

        stop = Stop(uuid4(), randword(), down, up, bus_up=bus_up)
        stops.append(stop)
    routes.append(Route(uuid4(), number=number, stops=stops))
routes.sort()


def get_route(id: str) -> Route:
    for route in routes:
        if str(route.id) == id:
            return route
    raise RuntimeError(f"Route with id '{id}' not found")
