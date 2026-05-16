<<<<<<< HEAD
=======
from dotenv import load_dotenv
import os
import logging
from telegram import *
import requests
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from functions import db,req
import time
>>>>>>> test
import json
import logging
import os
import time
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import Application, CommandHandler, ContextTypes

from functions import db, req

load_dotenv()
<<<<<<< HEAD

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID_RAW = os.getenv("ADMIN_CHAT_ID", "0")

=======
ASK_PASWD = 1
# --- НАСТРОЙКИ ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))  # Замените на ваш реальный Telegram ID
PASWD = os.getenv("PASSWORD")
# -----------------
>>>>>>> test
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing in environment variables.")

try:
    ADMIN_CHAT_ID = int(ADMIN_CHAT_ID_RAW)
    if ADMIN_CHAT_ID <= 0:
        raise ValueError
except ValueError:
    raise ValueError("ADMIN_CHAT_ID must be a valid positive integer.")

try:
    response = requests.get('http://10.9.0.1:5000/ping', timeout=5.0)
    response.raise_for_status()
    if response.text.strip() != '1488':
        raise ValueError("VPN server returned an invalid health check token.")
except (requests.RequestException, ValueError) as server_error:
    raise ConnectionError(f"VPN health check failed: {server_error}")


async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return

    user = update.effective_user
    username_info = f"@{user.username}" if user.username else user.full_name

    admin_message = (
        f"🚀 Новый пользователь запустил бота!\n"
        f"👤 Имя: {user.full_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"📝 Username: {username_info}"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
<<<<<<< HEAD
            text=admin_message,
            parse_mode="HTML"
        )
        logging.info("Notification sent for User ID: %s", user.id)
    except TelegramError as telegram_err:
        logging.error("Failed to notify admin via Telegram: %s", telegram_err)

    expiration_timestamp = int(time.time()) + 155_520_000
    user_payload = {
        "user_id": user.id,
        "time": expiration_timestamp
    }

    try:
        db.ins([user.id, expiration_timestamp])
    except Exception as db_err:
        logging.error("Database insertion failed for user %s: %s", user.id, db_err)
        await update.message.reply_text("Произошла ошибка при регистрации. Попробуйте позже.")
        return

    try:
        serialized_payload = json.dumps(user_payload)
        api_response_raw = await req.add_i(serialized_payload)
        
        if not api_response_raw:
            raise ValueError("Empty response received from API.")
            
        api_response = json.loads(api_response_raw)
        
        vpn_uri = api_response.get("vpnuri", "N/A")
        vpn_conf = api_response.get("conf", "N/A")
        
        await update.message.reply_text(
            f"Привет, {user.first_name}! vpnuri: {vpn_uri}, conf: {vpn_conf}"
        )
    except (json.JSONDecodeError, TypeError, KeyError, ValueError) as api_err:
        logging.error("API configuration fetching failed for user %s: %s", user.id, api_err)
        await update.message.reply_text("Не удалось сгенерировать конфигурацию VPN. Обратитесь к администратору.")

=======
            text=admin_message
            )
        logging.info(f"Имя: {user.full_name}\n, ID: {user.id}, Username: {user_info}")
    except Exception as e:
        logging.error(f"Не удалось отправить уведомление админу: {e}")
    # 3. Отвечаем самому пользователю
    if db.search(user.id) == None:
        await update.message.reply_text("Введи пароль. без него не пущу - или введи рандомную х  ню, чтобы отменить")
        logging.info(f"незарегистрированный пользователь {user.id} нажал /start")
        return ASK_PASWD
    else:
        await update.message.reply_text(
            f"Привет, {user.first_name}! ты уже зарегистрирован, не спамь, иначе заспамлю пинками твою мать!")
async def get_paswd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    paswd=update.message.text
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
    logging.info(f"пользователь {user.id} ввел пароль и зарегался")
    return ConversationHandler.END
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ты решил отменить ввод пароля"
    )
    return ConversationHandler.END
>>>>>>> test

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", handle_start_command))
    
    logging.info("Бот запущен и ждет сообщений...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


<<<<<<< HEAD
if __name__ == "__main__":
    main()
=======
# Создаем приложение
application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчик команды /start
conv_handler = ConversationHandler(
        # Точка входа в диалог (команда /start)
        entry_points=[CommandHandler('start', start)],
        # Состояния и обработчики для каждого состояния
        states={
            ASK_PASWD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_paswd)],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
        # Обработчики на случай выхода из диалога (например, команда /cancel)
    )

    # Запускаем бота (polling)
logging.info("Бот запущен и ждет сообщений...")
application.add_handler(conv_handler)
application.run_polling(allowed_updates=Update.ALL_TYPES)

#БОТ В СОСТОЯНИИ ЗИГОТЫ. ДОПИЛИТЬ.
>>>>>>> test
