from os import environ
from dotenv import load_dotenv
from typing import Final


class EnvironmentVariables:
    load_dotenv()
    DROPBOX_KEY: Final = environ.get('DROPBOX_KEY')
    BOT_TOKEN: Final = environ.get('BOT_TOKEN')
    FOLDER_PATH: Final = environ.get('FOLDER_PATH')
