from dotenv import load_dotenv
import os
import logging
from telegram import *
import httpx
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
import db  # локальная библиотека
import time
import json
import sys


# добавляет пользователей в vpn-сервер
async def add_i(pload):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post('http://10.9.0.1:5000/add', json=pload)
            return response.json()
        except httpx.ConnectError as err:
            return err


load_dotenv()
ASK_PASWD = 1


BOT_TOKEN = os.getenv("BOT_TOKEN")
# время, на которое будут добавляться ключи vpn
DEFAULT_TIME = int(os.getenv("DEFAULT_TIME"))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))
PASWD = os.getenv("PASSWORD")  # пароль для получения ключа бота


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# проверка
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")
if not ADMIN_CHAT_ID:
    raise ValueError("ADMIN_CHAT_ID не найден в переменных окружения!")
if not PASWD:
    raise ValueError("PASSWORD не найден в переменных окружения!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_info = f"@{user.username}" if user.username else f"{user.full_name}"

    admin_message = (
        f"🚀 Новый пользователь запустил бота!\n"
        f"👤 Имя: {user.full_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"📝 Username: {user_info}"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message
        )
        logging.info(
            f"Имя: {
                user.full_name}\n, ID: {
                user.id}, Username: {user_info}")
    except Exception as e:
        logging.error(f"Не удалось отправить уведомление админу: {e}")
    # 3. Отвечаем самому пользователю
    if db.search(user.id) is None:
        await update.message.reply_text("Введи пароль. без него не пущу - или введи /cancel, чтобы отменить")
        logging.info(
            f"незарегистрированный пользователь {
                user.id} нажал /start")
        return ASK_PASWD
    else:
        await update.message.reply_text(
            f"Привет, {user.first_name}! ты уже зарегистрирован")


async def get_paswd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # проверяем пароль
    user = update.effective_user
    paswd = update.message.text
    time_v = (int(time.time()) + DEFAULT_TIME)
    pload = {
        "user_id": update.effective_user.id,
        "time": time_v
    }
    db_data = [user.id, time_v]
    db.ins(db_data)
    request = await add_i(pload)
    if isinstance(request, Exception):
        await update.message.reply_text("Ведутся техработы. извиняюсь и стою на коленях. попробуйте позже")
        logging.error("сервер с vpn недоступен")
    else:
        if paswd == PASWD:
            await update.message.reply_text(
                f"vpnuri:  {request["vpnuri"]}, conf:  {request["conf"]}")
            logging.info(f"пользователь {user.id} ввел пароль и зарегался")
        else:
            await update.message.reply_text("ты ввел неверный пароль")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ты решил отменить ввод пароля"
    )
    return ConversationHandler.END


# Создаем приложение
application = Application.builder().token(BOT_TOKEN).build()

# Регистрируем обработчик команды /start
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    # Состояния и обработчики для каждого состояния
    states={
        ASK_PASWD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_paswd)],

    },
    fallbacks=[CommandHandler('cancel', cancel)],
    # Обработчики на случай выхода из диалога (например, команда /cancel)
)

logging.info("Бот запущен и ждет сообщений...")
application.add_handler(conv_handler)
application.run_polling(allowed_updates=Update.ALL_TYPES)
