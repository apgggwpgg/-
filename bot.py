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

# Планировщик
scheduler = AsyncIOScheduler()

# Генерация расписания
async def send_schedule():
    global current_week
    rotation = users[current_week % len(users):] + users[:current_week % len(users)]
    assignments = list(zip(zones, rotation))
    message = "🧹 Расписание уборки на неделю:\n\n"
    for zone, person in assignments:
        message += f"{zone}: {person}\n"
    await application.bot.send_message(chat_id=CHAT_ID, text=message)
    current_week += 1

# Команда /start
async def start(update, context):
    await update.message.reply_text("Бот запущен! Используй /schedule чтобы увидеть текущее расписание.")

# Команда /schedule
async def schedule_command(update, context):
    rotation = users[current_week % len(users):] + users[:current_week % len(users)]
    assignments = list(zip(zones, rotation))
    message = "🧹 Расписание уборки на неделю:\n\n"
    for zone, person in assignments:
        message += f"{zone}: {person}\n"
    await update.message.reply_text(message)

# Создание приложения
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("schedule", schedule_command))

# Функция запуска
async def main():
    scheduler.add_job(send_schedule, "interval", weeks=1)
    scheduler.start()
    await application.run_polling()

# Запуск
if __name__ == "__main__":
    import asyncio
    print("Бот запускается...")
    asyncio.run(main())
