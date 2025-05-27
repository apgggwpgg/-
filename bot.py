import os
import datetime
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# — Логирование
logging.basicConfig(level=logging.INFO)

# — Чтение из окружения
TOKEN   = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])

# — Участники и зоны
people = ["Гена", "Рома", "Алан"]
zones  = ["Ванна и туалет", "Кухня", "Коридор"]
BASE_DATE = datetime.date(2025, 1, 1)

# — Генерация текста расписания
def render_schedule_text():
    today = datetime.date.today()
    weeks_passed = (today - BASE_DATE).days // 7
    offset = weeks_passed % len(people)
    lines = ["🧹 Расписание уборки на неделю:\n"]
    for i, zone in enumerate(zones):
        person = people[(i + offset) % len(people)]
        lines.append(f"▪ {zone}: {person}")
    return "\n".join(lines)

# — Обработчик /schedule
async def schedule_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(render_schedule_text())

# — Функция для планировщика
async def send_weekly_schedule():
    await application.bot.send_message(chat_id=CHAT_ID, text=render_schedule_text())

# === Настройка бота и планировщика ===

# Создаём приложение
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("schedule", schedule_command))

# Настраиваем APScheduler
scheduler = AsyncIOScheduler()
scheduler.add_job(
    send_weekly_schedule,
    trigger="cron",
    day_of_week="mon",
    hour=9,
    minute=0
)
scheduler.start()

# === Запуск бота ===
if __name__ == "__main__":
    logging.info("Стартуем бот и запускаем polling...")
    # .run_polling() самостоятельно запускает asyncio loop и не закрывает его некорректно
    application.run_polling()

