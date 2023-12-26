# Исходный код бота группы "ПсковГу БОТ"
Создавался в рамках проектной деятельности в университете, но в итоге вырос.

Основная цель – оперативное получение и обновление информации о изменениях в расписании ([оригинальное расписание](https://rasp.pskgu.ru/) содержит html страницы, которые кешируются браузерами)

# Запуск

Можно запустить либо напрямую
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn pskgu_bot.main:app
```
либо через докер (есть Dockerfile)

## Настройки
в файле config.py прописаны настройки проекта.

Для запуска нужно создать переменные среды:
```bash
export TOKEN_VK="secret_group_token"
export GROUP_ID=id_group
export MONGO_URL="mongodb://localhost:27017"
```

# Особенности
- Используется MongoDB для хранения записей о расписании.

- Проект состоит из двух частей
  1. вк бот (папка bots)

    Вк бот Написан с использованием [vkbottle](https://github.com/vkbottle/vkbottle)

  2. парсер (папка parser)

    Использует [lxml xpath](https://lxml.de/xpathxslt.html#xpath), [aiohttp client](https://docs.aiohttp.org/en/stable/client.html) для асинхроноого и быстрого парсинга оригинального сайта расписания. 

> p.s. для работы в heroku/render нужен был веб сервис, поэтому есть fastapi и cron по пингу сайта

# Полезные ссылки

- [группа вк](https://vk.com/pskgu_bot)
- [апи расписания](https://github.com/mrgick/pskgu_api)
- [альтернативный сайт расписания](https://github.com/mrgick/rasp_pskgu)
