"""
    Настроки бота
"""

import os


class Config:
    """
        Класс настроек
    """
    # настроки парсера
    STOP_PARSER = os.environ.get('STOP_PARSER')
    REMOTE_URL = "http://rasp.pskgu.ru"
    SEMAPHORE = 40

    # настроки mongo db
    DB_NAME = "DB"
    MAX_POOL_SIZE = 50
    MONGO_URI = os.environ.get('MONGO_URL')

    # настроки вк бота
    VK_TOKEN = os.environ.get('TOKEN_VK')
    GROUP_ID = os.environ.get('GROUP_ID')

    # web
    WEB_URL = "https://mrgick.github.io/rasp_pskgu/index.html"

    # настройки cron
    CRON_PERIOD = 5*60
    URL_PING = os.environ.get('URL_PING', 'https://127.0.0.1')
