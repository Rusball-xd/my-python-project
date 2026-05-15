from dotenv import load_dotenv
import os
import logging
from telegram import *
import requests
from telegram.ext import Application, CommandHandler
from functions import db,req
load_dotenv()
# --- НАСТРОЙКИ ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))  # Замените на ваш реальный Telegram ID
# -----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
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
            text=admin_message)
        logging.info(f"Имя: {user.full_name}\n, ID: {user.id}, Username: {user_info}")
    except Exception as e:
        logging.error(f"Не удалось отправить уведомление админу: {e}")
    # 3. Отвечаем самому пользователю
    time = (int(time.time())+ 155520000)
    g = {
        "user_id": update.effective_user.id,
         "time":time
         }
    k = [user.id, time]
    db.ins(k)
    request = req.add_i(json.dumps(g))
    request = json.loads(request)
    await update.message.reply_text(
        f"Привет, {user.first_name}!  у тебя мать шлюха! vpnuri:{request["vpnuri"]}, conf:{request["conf"]}")




# Создаем приложение
application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчик команды /start
application.add_handler(CommandHandler("start", start))

    # Запускаем бота (polling)
logging.info("Бот запущен и ждет сообщений...")
application.run_polling(allowed_updates=Update.ALL_TYPES)

#БОТ В СОСТОЯНИИ ЗИГОТЫ. ДОПИЛИТЬ.
