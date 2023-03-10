import logging
from aiogram import Dispatcher, Bot, types, executor
from bot.handlers import register_all_handlers

from bot.misc import TgKeys


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_handlers(dp)


def start_bot():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TgKeys.API_TOKEN)
    dp = Dispatcher(bot)

    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
