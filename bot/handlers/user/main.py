import redis
from bot.misc import dropbox
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from bot.keyboards import get_main_keyboard, send_picture_to_database_confirmation_keyboard
from bot.misc import EnvironmentVariables
from bot.misc.dropbox import connect_to_dropbox, show_all_pictures

love_emoji = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '❤️‍🔥',
              '❣️', '💕', '💞', '💓', '💗', '💖', '💘', '💝', '😍', '🥰',
              '😘', '😻', '😽', '💋']


async def __say_hi(msg: Message) -> None:
    """
    This handler will be called when user sends `/start` or `/hi` command
    """
    bot: Bot = msg.bot
    markup = get_main_keyboard()
    await bot.send_message(msg.chat.id, f'(=^_^=)/ ~~  <i>Hii, {msg.from_user.first_name}</i>',
                           parse_mode='html', reply_markup=markup)


async def __help(msg: Message) -> None:
    """
    This handler will call command list when user sends `/help` command
    """
    bot: Bot = msg.bot
    reply_markup = get_main_keyboard()
    await bot.send_message(msg.chat.id, 'I\'ll help you, what do you want?', reply_markup=reply_markup)
    await bot.send_message(msg.chat.id, 'Command List:\n'
                                        '/catpic - send random picture of a cat\n'
                                        '/hi - say "hi"\n'
                                        '/subscribe - subscribe to my hourly pics sending'
                                        '*any heart emoji* - send this if you love me\n')


async def __send_catpic(msg: Message) -> None:
    """
    Sends random picture of a cat when user sends `/catpic` command
    """
    bot: Bot = msg.bot
    wait_warning = await bot.send_message(chat_id=msg.chat.id, text='Wait a little bit, please')
    dbx = connect_to_dropbox()
    files = show_all_pictures(dbx)
    try:
        image_link = dropbox.find_random_picture(files, dbx)
        if image_link:
            await bot.send_photo(msg.chat.id, image_link)
        else:
            await msg.reply('I do not have any pics right now \U0001F63F')
    except Exception as e:
        await bot.send_message(msg.chat.id, f'Something went wrong :(')
    await bot.delete_message(chat_id=msg.chat.id, message_id=wait_warning.message_id)


async def __subscribe_to_catpics(msg: Message):
    """
    Subscribes or unsubscribes user to the hourly cat-picture sending after using `/subscribe` command
    """
    bot: Bot = msg.bot
    try:
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        chat_id = msg.chat.id
        is_subscribed = redis_client.sismember('subscribers', chat_id)
        if is_subscribed:
            await bot.send_message(chat_id, 'You are no longer my subscriber')
            redis_client.srem('subscribers', chat_id)
        else:
            redis_client.sadd('subscribers', chat_id)
            await bot.send_message(chat_id, 'You are my subscriber now')
    except Exception as e:
        print(e)
        await bot.send_message(msg.chat.id, f'Something went wrong :(')


async def __react_on_heart(msg: Message) -> None:
    """
    Answers on text with hearth emoji
    """
    bot: Bot = msg.bot
    text = msg.text.split()
    if any(element in text for element in love_emoji):
        await bot.send_message(msg.chat.id, 'Ooh~ I love you too, my darling \U0001F63D')
    else:
        await bot.send_message(msg.chat.id, 'Meow? I don\'t understand you')


async def __react_on_photo(msg: Message) -> None:
    """
    Answers on photo
    """
    bot: Bot = msg.bot
    inline_markup = send_picture_to_database_confirmation_keyboard()
    await bot.send_message(msg.chat.id, 'Cool! May I add it to my database? \U0001F63C',
                           reply_markup=inline_markup)


async def __add_to_database_callback(call: CallbackQuery) -> None:
    """
    Confirm adding picture by user
    """
    bot: Bot = call.bot
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    if call.data == 'OKButton':
        previous_message_id = call.message.message_id - 1
        await bot.forward_message(chat_id=EnvironmentVariables.ADMIN_CHAT_ID,
                                  from_chat_id=call.message.chat.id,
                                  message_id=previous_message_id)
        await call.message.answer('I\'ll add your picture after passing the moderation \U0001F63C')
    elif call.data == 'CancelButton':
        await call.message.answer('Ok, honey. I won\'t add it')


def register_users_handlers(dp: Dispatcher) -> None:
    """
    Register all user's handlers
    """
    dp.register_message_handler(__say_hi, commands=['start', 'hi'])
    dp.register_message_handler(__help, commands=['help'])
    dp.register_message_handler(__send_catpic, commands=['catpic'])
    dp.register_message_handler(__subscribe_to_catpics, commands=['subscribe'])
    dp.register_message_handler(__react_on_heart, content_types=['text'])
    dp.register_message_handler(__react_on_photo, content_types=['photo'])
    dp.register_callback_query_handler(__add_to_database_callback)
