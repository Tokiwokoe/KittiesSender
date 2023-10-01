from os import environ
from dotenv import load_dotenv
from typing import Final


class EnvironmentVariables:
    load_dotenv()
    DROPBOX_KEY: Final = environ.get('DROPBOX_KEY')
    BOT_TOKEN: Final = environ.get('BOT_TOKEN')
    FOLDER_PATH: Final = environ.get('FOLDER_PATH')
    ADMIN_CHAT_ID: Final = environ.get('ADMIN_CHAT_ID')
    APP_KEY: Final = environ.get('APP_KEY')
    APP_SECRET: Final = environ.get('APP_SECRET')
    REFRESH_TOKEN: Final = environ.get('REFRESH_TOKEN')
