import logging
from aiogram import Dispatcher, Bot, executor
from bot.handlers import register_all_handlers
from bot.misc import EnvironmentVariables
from bot.tasks import send_catpic_task


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_handlers(dp)


def start_bot():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=EnvironmentVariables.BOT_TOKEN)
    dp = Dispatcher(bot)
    #send_catpic_task.delay()
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
