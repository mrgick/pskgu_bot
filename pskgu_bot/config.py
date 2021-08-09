"""
    Настроки бота
"""

import os


class Config:
    """
        Класс настроек
    """
    # настроки парсера
    REMOTE_URL = "http://rasp.pskgu.ru"
    SEMAPHORE = 40
    YEAR = 2021

    # настрокий mongodb
    DB_NAME = "DB"
    MAX_POOL_SIZE = 100
    MONGO_URI = os.environ.get('MONGO_URL')

    # настроки вк бота
    VK_TOKEN = os.environ.get('TOKEN_VK')
    GROUP_ID = os.environ.get('GROUP_ID')
