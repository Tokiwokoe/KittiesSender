import os
import random

from aiogram import Bot, Dispatcher
from aiogram.types import Message


love_emoji = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '❤️‍🔥',
              '❣️', '💕', '💞', '💓', '💗', '💖', '💘', '💝', '😍', '🥰',
              '😘', '😻', '😽', '💋']


async def __say_hi(msg: Message) -> None:
    """
    This handler will be called when user sends `/start` or `/hi` command
    """
    bot: Bot = msg.bot
    user_id = msg.from_user.id
    await bot.send_message(msg.chat.id, f'(=^_^=)/ ~~  <i>Hii, {msg.from_user.first_name}</i>',
                           parse_mode='html')


async def __help(msg: Message) -> None:
    """
    This handler will call command list when user sends `/help` command
    """
    bot: Bot = msg.bot
    user_id = msg.from_user.id
    photo = open('catpics/halp.jpg', 'rb')
    await bot.send_message(msg.chat.id, 'I\'ll help you, what do you want?', reply_markup=markup)
    await bot.send_message(msg.chat.id, 'Command List:\n /catpic - send random picture of a cat\n /hi - say "hi"\n *any heart emoji* - send this if you love me\n')
    await bot.send_photo(msg.chat.id, photo)


async def __send_catpic(msg: Message):
    """
    Sends random picture of a cat when user sends `/catpic` or `/cat` command
    """
    bot: Bot = msg.bot
    user_id = msg.from_user.id
    try:
        img_list = os.listdir('bot/catpics/')
        img_path = f'bot/catpics/{random.choice(img_list)}'
        photo = open(img_path, 'rb')
        await bot.send_photo(msg.chat.id, photo=photo)
    except FileNotFoundError:
        await msg.reply('I do not have any pics right now \U0001F63F')


async def __react_on_heart(msg: Message):
    """
    Answers on text with hearth emoji
    """
    bot: Bot = msg.bot
    user_id = msg.from_user.id
    if msg.text in love_emoji:
        await bot.send_message(msg.chat.id, 'Ooh~ I love you too, my darling \U0001F63D')
    else:
        await bot.send_message(msg.chat.id, 'Meow?')


async def __react_on_photo(msg: Message):
    """
    Answers on photo
    """
    bot: Bot = msg.bot
    user_id = msg.from_user.id
    await bot.send_message(msg.chat.id, 'Cool! Here\'s mine \U0001F63C')
    photo = open('catpics/Kitty.jpg', 'rb')
    await bot.send_photo(msg.chat.id, photo)


def register_users_handlers(dp: Dispatcher) -> None:

    dp.register_message_handler(__say_hi, commands=['start', 'hi'])
    dp.register_message_handler(__help, commands=['help'])
    dp.register_message_handler(__send_catpic, commands=['catpic'])
    dp.register_message_handler(__react_on_heart, content_types=['text'])
    dp.message_handler(__react_on_photo, content_types=['photo'])
