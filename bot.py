from telegram.ext import Application, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import os
import logging

# Логирование
logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

# Данные
users = ["Алан", "Гена", "Рома"]
zones = ["Ванна/Туалет", "Кухня", "Коридор"]
current_week = 0

# Расписание
async def send_schedule():
    global current_week
    rotation = users[current_week % len(users):] + users[:current_week % len(users)]
    assignments = list(zip(zones, rotation))
    message = "🧹 Расписание уборки на неделю:\n\n"
    for zone, person in assignments:
        message += f"{zone}: {person}\n"
    await application.bot.send_message(chat_id=CHAT_ID, text=message)
    current_week += 1

# /start
async def start(update, context):
    await update.message.reply_text("Бот запущен! Расписание будет приходить каждую неделю.")

# Инициализация
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Планировщик
scheduler = AsyncIOScheduler()
scheduler.add_job(send_schedule, "interval", weeks=1)
scheduler.start()

# Запуск
if __name__ == "__main__":
    print("Бот запущен")
    application.run_polling()
