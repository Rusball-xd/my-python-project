from dotenv import load_dotenv
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
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
    """
    Обработчик команды /start.
    Отправляет уведомление админу и отвечает пользователю.
    """
    user = update.effective_user
    user_info = f"@{user.username}" if user.username else f"{user.full_name}"

    # 1. Формируем сообщение для админа
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
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n"
        f"Твой запрос принят. Я сообщил о тебе куда следует (пора не пора идут мусора)"
    )


    # Создаем приложение
application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчик команды /start
application.add_handler(CommandHandler("start", start))

    # Запускаем бота (polling)
logging.info("Бот запущен и ждет сообщений...")
application.run_polling(allowed_updates=Update.ALL_TYPES)

#БОТ В СОСТОЯНИИ ЗИГОТЫ. ДОПИЛИТЬ.
