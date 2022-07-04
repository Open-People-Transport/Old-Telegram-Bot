from dataclasses import dataclass

from telegram import InlineKeyboardMarkup


@dataclass
class Page:
    message: str
    keyboard: InlineKeyboardMarkup
