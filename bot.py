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

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID_RAW = os.getenv("ADMIN_CHAT_ID", "0")

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


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", handle_start_command))
    
    logging.info("Бот запущен и ждет сообщений...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
