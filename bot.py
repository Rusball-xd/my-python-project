from dotenv import load_dotenv
import os
import logging
from telegram import *
import requests
from telegram.ext import Application, CommandHandler
from functions import db,req
import time
import json
load_dotenv()
# --- НАСТРОЙКИ ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))  # Замените на ваш реальный Telegram ID
# -----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
if requests.get('http://10.9.0.1:5000/ping').text != '1488':
    raise ValueError("У ТЕБЯ НЕ РАБОТАЕТ СЕРВЕР С ВПН, ДАУН!")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")
if not ADMIN_CHAT_ID:
    raise ValueError("ADMIN_CHAT_ID не найден в переменных окружения!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    user_info = f"@{user.username}" if user.username else f"{user.full_name}"

    admin_message = (
        f"🚀 Новый пользователь запустил бота!\n"
        f"👤 Имя: {user.full_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"📝 Username: {user_info}"
    )

    # 2. Отправляем уведомление на указанный ID
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message
            )
        logging.info(f"Имя: {user.full_name}\n, ID: {user.id}, Username: {user_info}")
    except Exception as e:
        logging.error(f"Не удалось отправить уведомление админу: {e}")
    # 3. Отвечаем самому пользователю
    if db.search(user.id) == None:
        vremya = (int(time.time())+ 155520000)
        g = {
            "user_id": update.effective_user.id,
            "time":vremya
            }
        k = [user.id, vremya]
        db.ins(k)
            request = await req.add_i(g)
        await update.message.reply_text(
            f"Привет, {user.first_name}!  vpnuri:  {request["vpnuri"]}, conf:  {request["conf"]}")
    else:
        await update.message.reply_text(
            f"Привет, {user.first_name}! ты уже зарегистрирован, не спамь, иначе заспамлю ударами твою мать!"




# Создаем приложение
application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчик команды /start
application.add_handler(CommandHandler("start", start))

    # Запускаем бота (polling)
logging.info("Бот запущен и ждет сообщений...")
application.run_polling(allowed_updates=Update.ALL_TYPES)

#БОТ В СОСТОЯНИИ ЗИГОТЫ. ДОПИЛИТЬ.
