"""
    Запуск проекта (main-файл).
"""

import asyncio
from fastapi import FastAPI, Query, Request, Response

from pskgu_bot.config import Config
from pskgu_bot.utils import logger
from pskgu_bot.db.services import initialize_storage
from pskgu_bot.bots.vk_bot.run import run_vk_bot
from pskgu_bot.parser.run import run_parser
from pskgu_bot.cron import run_cron

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await initialize_storage()
    await bot_wrap()
    await run_cron()


@app.get("/")
async def index(request: Request, response: Response):
    return {"status": "200"}


@app.get("/ping")
async def test_connection(request: Request, response: Response):
    return {"status": "200"}


async def bot_wrap():
    loop = asyncio.get_event_loop()
    loop.create_task(run_vk_bot())
    if Config.STOP_PARSER != "stop":
        logger.info("running parser module")
        loop.create_task(run_parser())
