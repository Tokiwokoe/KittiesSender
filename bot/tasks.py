import asyncio
import redis
from bot.misc import dropbox
from bot.misc.env import EnvironmentVariables
from aiogram import Bot
from bot.misc.dropbox import connect_to_dropbox, show_all_pictures
from bot.celery import app


celery_event_loop = asyncio.new_event_loop()


async def send_plan_catpic():
    print('Task runs')
    bot = Bot(token=EnvironmentVariables.BOT_TOKEN)

    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    subscribers = redis_client.smembers('subscribers')
    subscribers_list = [int(chat_id) for chat_id in subscribers]
    dbx = connect_to_dropbox()
    files = show_all_pictures(dbx)

    for chat_id in subscribers_list:
        try:
            image_link = dropbox.find_random_picture(files, dbx)
            if image_link:
                await bot.send_photo(chat_id, image_link)
            else:
                await bot.send_message(chat_id, 'I do not have any pics right now \U0001F63F')
        except Exception as e:
            await bot.send_message(chat_id, 'Something went wrong :(')
            print(e)


@app.task
def send_catpic_task() -> None:
    # celery -A bot beat -l info
    # celery -A bot worker --loglevel=INFO --pool=solo
    celery_event_loop.run_until_complete(send_plan_catpic())
