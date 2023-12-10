import logging.config
import os
import re
from typing import Tuple

from langchain.chat_models.gigachat import GigaChat

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
    },

    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}

logging.config.dictConfig(LOGGING)


class Settings:
    telegram_bot_token: str
    storage_file_path: str
    state_file_path: str

    gigachat_credential: str = os.environ.get('GIGACHAT_CREDENTIAL')

    def __init__(self):
        self.telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')

        if not self.telegram_bot_token:
            raise Exception('Укажите телеграмм токен в переменную окружения TELEGRAM_BOT_TOKEN,'
                            ' https://core.telegram.org/bots#6-botfather')



        self.state_file_path = './user_states'


settings = Settings()

chat_model = GigaChat(
    credentials=settings.gigachat_credential,
    verify_ssl_certs=False
)