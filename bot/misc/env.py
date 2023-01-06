from os import environ
from typing import Final


class TgKeys:
    API_TOKEN: Final = environ.get('API_TOKEN', 'define me!')
