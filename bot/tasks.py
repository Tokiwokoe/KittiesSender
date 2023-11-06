import asyncio
import redis
from bot.misc.env import EnvironmentVariables
from aiogram import Bot
from bot.misc import dropbox
from bot.celery import app


celery_event_loop = asyncio.new_event_loop()


async def send_plan_catpic():
    print('Task runs')
    bot = Bot(token=EnvironmentVariables.BOT_TOKEN)

    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    subscribers = redis_client.smembers('subscribers')
    subscribers_list = [int(chat_id) for chat_id in subscribers]

    for chat_id in subscribers_list:
        try:
            image_link = dropbox.find_random_picture()
            if image_link:
                await bot.send_photo(chat_id, image_link)
            else:
                await bot.send_message(chat_id, 'I do not have any pics right now \U0001F63F')
            print(chat_id)
        except Exception as e:
            await bot.send_message(chat_id, 'Something went wrong :(')


@app.task
def send_catpic_task() -> None:
    celery_event_loop.run_until_complete(send_plan_catpic())
