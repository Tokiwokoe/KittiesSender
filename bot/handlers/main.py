from aiogram import Dispatcher

from bot.handlers.user.main import register_users_handlers


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_users_handlers,
    )
    for handler in handlers:
        handler(dp)
