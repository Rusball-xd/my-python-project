from dotenv import load_dotenv
import os
import logging
import requests
from functions import db
import time
import json
from aiogram import Bot, Dispatcher
from aiogram.types import Message        # [1]
import asyncio                           # [1]

async def add_i(b):
    g = requests.post('http://10.9.0.1:5000/add', json=b).json()
    return g

dp = Dispatcher()
load_dotenv()
ASK_PASWD = 1
# --- НАСТРОЙКИ ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))  # Замените на ваш реальный Telegram ID
PASWD = os.getenv("PASSWORD")
# -----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
#if requests.get('http://10.9.0.1:5000/ping').text != '1488':
#    raise ValueError("У ТЕБЯ НЕ РАБОТАЕТ СЕРВЕР С ВПН, ДАУН!")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")
if not ADMIN_CHAT_ID:
    raise ValueError("ADMIN_CHAT_ID не найден в переменных окружения!")
import asyncio                           # [1]


dp = Dispatcher()                        # [2]


@dp.message()                            # [3]
async def any_message(                   # [4]
        message: Message,                # [5]
):
    await message.answer("Hello world!") # [6]


async def main():
    token = BOT_TOKEN          # [7]
    if not token:                        # [7]
        error = "No token provided"      # [7]
        raise ValueError(error)          # [7]
    bot = Bot(token=token)               # [8]

    print("Starting bot...")
    try:
        await dp.start_polling(bot)      # [9]
    finally:
        print("Bot stopped")


asyncio.run(main())

    # Запускаем бота (polling)
logging.info("Бот запущен и ждет сообщений...")


