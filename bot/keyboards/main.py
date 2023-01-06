from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup()
    heart_button = KeyboardButton('💖')
    catpic_button = KeyboardButton('/catpic')
    help_button = KeyboardButton('/help')
    markup.add(catpic_button, help_button, heart_button)
    return markup
