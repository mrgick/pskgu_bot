#!/bin/sh

# Список экспортируемых переменных окружения для settings.cfg.

# Токен для бота в ВК (обязательно для ВК)
export VK_API_TOKEN

# Идентификатор группы бота в ВК (обязательно для ВК) 
export VK_GROUP_ID

# Ссылка для mongodb (обязательно для mongodb)
export MONGODB_URL

# Название базы данных mongodb (обязательно для mongodb)
export MONGODB_NAME

# Сайт расписания (по умолчанию rasp.pskgu.ru)
export SCHEDULE_URL="http://rasp.pskgu.ru"

# Файл логов 
export LOGFILE="logs/recent.txt"

# Версия бота 
export VERSION_MAJOR=3
export VERSION_MINOR=0

# Режим отладки (по умолчанию выключен)
export DEBUG=0

# Исполняемый файл python (по умолчанию python)
export PYTHON_EXEC=python

# Запускной py файл (по умолчанию ./main.py)
export MAIN_PY=./main.py

# Опции запуска (опционально)
export LAUNCH_OPTS=""
