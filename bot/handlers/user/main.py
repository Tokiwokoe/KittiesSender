import random
import dropbox
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from bot.keyboards import get_main_keyboard, send_picture_to_database_confirmation_keyboard
from bot.misc import EnvironmentVariables

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
                                        '*any heart emoji* - send this if you love me\n')


async def __send_catpic(msg: Message) -> None:
    """
    Sends random picture of a cat when user sends `/catpic` command
    """
    bot: Bot = msg.bot
    dbx = dropbox.Dropbox(EnvironmentVariables.DROPBOX_KEY)

    try:
        folder_path = '/KittiesSender'
        files = dbx.files_list_folder(folder_path).entries

        if files:
            random_image = random.choice(files)
            image_link = dbx.sharing_create_shared_link(random_image.path_display).url
            await bot.send_photo(msg.chat.id, image_link)
        else:
            await msg.reply('I do not have any pics right now \U0001F63F')
    except Exception as e:
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
        await bot.forward_message(6264984720, from_chat_id=call.message.chat.id, message_id=previous_message_id)
        await call.message.answer('I\'ll add your picture after passing the moderation \U0001F63C')
    elif call.data == 'CancelButton':
        await call.message.answer('Ok, honey. I won\'t add it')


async def __confirm_users_picture_sending(msg: Message) -> None:
    """
    Confirm adding picture by admin
    """
    pass


def register_users_handlers(dp: Dispatcher) -> None:
    """
    Register all user's handlers
    """
    dp.register_message_handler(__say_hi, commands=['start', 'hi'])
    dp.register_message_handler(__help, commands=['help'])
    dp.register_message_handler(__send_catpic, commands=['catpic'])
    dp.register_message_handler(__react_on_heart, content_types=['text'])
    dp.register_message_handler(__react_on_photo, content_types=['photo'])
    dp.register_message_handler(__confirm_users_picture_sending, )
    dp.register_callback_query_handler(__add_to_database_callback)
