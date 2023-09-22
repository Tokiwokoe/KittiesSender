from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup()
    markup.add(
        KeyboardButton('💖'),
        KeyboardButton('/catpic'),
        KeyboardButton('/help')
    )
    return markup


def send_picture_to_database_confirmation_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(1)
    markup.add(
        InlineKeyboardButton('✅', callback_data='OKButton'),
        InlineKeyboardButton('❌', callback_data='CancelButton'),
    )
    return markup


def admin_send_picture_to_database_confirmation_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(1)
    markup.add(
        InlineKeyboardButton('✅', callback_data='OKButton'),
        InlineKeyboardButton('❌', callback_data='CancelButton'),
        InlineKeyboardButton('BAN', callback_data='BAN'),
    )
    return markup
