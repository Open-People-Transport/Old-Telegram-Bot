from typing import Any, Callable, Coroutine

from telegram import Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes

from .application import application

HandlerCallback = Callable[
    [Update, ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, None]
]
ErrorHandlerCallback = Callable[
    [object, ContextTypes.DEFAULT_TYPE], Coroutine[Any, Any, None]
]


class command_handler:
    def __init__(self, command: str) -> None:
        self.command = command

    def __call__(self, callback: HandlerCallback) -> Any:
        application.add_handler(
            CommandHandler(
                command=self.command,
                callback=callback,
            )
        )
        return callback


class callback_query_handler:
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def __call__(self, callback: HandlerCallback) -> Any:
        application.add_handler(
            CallbackQueryHandler(
                callback=callback,
                pattern=self.pattern,
            )
        )
        return callback


class error_handler:
    def __call__(self, callback: ErrorHandlerCallback) -> Any:
        application.add_error_handler(callback=callback)
        return callback
