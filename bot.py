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
CREDS= os.getenv("PAYMENT_CREDS")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# проверка
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")
if not ADMIN_CHAT_ID:
    raise ValueError("ADMIN_CHAT_ID не найден в переменных окружения!")
if not DEFAULT_TIME:
    raise ValueError("DEFAULT_TIME не найден в переменных окружения!")
if not CREDS:
    raise ValueError("PAYMENT_CREDS не найден в переменных окружения!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_status = db.check_for_status(user.id)
    if user_status == None:
        await update.message.reply_text(f"Добро пожаловать в моего бота! здесь ты можешь затариться vpn'ом. кидай деньги мне на карточку по номеру телефона СБП, и я дам тебе доступ. скидывать сюда: {CREDS}. в ответ напиши свои платежные данные - чтобы можно было проверить, заплатил ли ты")
        logging.info(
            f"незарегистрированный пользователь {
                user.id} нажал /start")
        return GET_PAYMENT

    elif user_status[2] == 0:
        await update.message.reply_text("админ скоро чекнет карточку и одобрит, stay calm")

    else:
        await update.message.reply_text(
            f"Привет, {user.first_name}! ты уже получил свой ключ, не трать мне CPU!")





async def give_access_promt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != ADMIN_CHAT_ID:
        return ConversationHandler.END
    await update.message.reply_text("введите id пользователя, которому хотите подтвердить оплату")
    return CONFIRM_PAYMENT_CHECK


async def give_access_ans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.text
    status = db.check_for_status(user)
    if status == None or status[2] == 1 :
        await update.message.reply_text("такого пользователя нет или он получил свой ключ! ")
        logging.info("нет такого пользователя")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Проверь свою карточку. если там появились деньги от пацанчика, который хотел. напиши y, если деньги получены, и n, если нет")
        context.user_data['user_id'] = user
        logging.info("проверяем карточку")
        return PAYMENT_YN





async def giving_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text=='y':
        user = context.user_data['user_id']
        time_v = (int(time.time()) + DEFAULT_TIME)
        pload = {
            "user_id": user,
            "time": time_v
        }
        request = await add_i(pload)
        if isinstance(request, Exception):
            await context.bot.send_message(chat_id = ADMIN_CHAT_ID, text="Ведутся техработы, сервер с vpn недоступен. извиняюсь и стою на коленях. попробуйте позже")
            logging.error("сервер с vpn недоступен")
        else:
            await context.bot.send_message(chat_id = user, text=
                f"vpnuri:  {request["vpnuri"]}, conf:  {request["conf"]}")
            logging.info(f"пользователь {user} ввел пароль и зарегался")
            db_data = [user, time_v]
            db.change_expiration(db_data)
            db.change_status(user, 1)

    return ConversationHandler.END


async def send_payment_noftification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = [user.id, 999999999999, 0]
    db.ins(data)
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"у тебя новый клиент! его карточка: {update.message.text}, его id: {user.id}")
    await update.message.reply_text("сейчас мы проверим твой платеж, и тогда отправим тебе ключ")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ты решил отменить текущую операцию"
    )
    return ConversationHandler.END


# Создаем приложение
application = Application.builder().token(BOT_TOKEN).build()
CONFIRM_PAYMENT_CHECK = 0
PAYMENT_YN = 1
GET_PAYMENT = 2
# Регистрируем обработчик команды /start
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start), CommandHandler('give_access', give_access_promt)],
    # Состояния и обработчики для каждого состояния
    states={
        CONFIRM_PAYMENT_CHECK: [MessageHandler(filters.TEXT & ~filters.COMMAND, give_access_ans)],
        PAYMENT_YN: [MessageHandler(filters.TEXT & ~filters.COMMAND, giving_access)],
        GET_PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_payment_noftification)],

    },
    fallbacks=[CommandHandler('cancel', cancel)],
    # Обработчики на случай выхода из диалога (например, команда /cancel)
)

logging.info("Бот запущен и ждет сообщений...")
application.add_handler(conv_handler)
application.run_polling(allowed_updates=Update.ALL_TYPES)
