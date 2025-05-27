import os
import datetime
import logging
import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# — Настройка логирования
logging.basicConfig(level=logging.INFO)

# — Чтение токена и чата из окружения
TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])

# — Ваши участники и зоны
people = ["Гена", "Рома", "Алан"]
zones  = ["Ванна и туалет", "Кухня", "Коридор"]

# — Опорная дата начала ротации (поставьте ту, когда у вас стартовал первый цикл)
BASE_DATE = datetime.date(2025, 1, 1)

def get_schedule_for_today():
    """Считает, сколько недель прошло с BASE_DATE, и выдаёт текущую ротацию."""
    today = datetime.date.today()
    weeks_passed = (today - BASE_DATE).days // 7
    offset = weeks_passed % len(people)
    result = {}
    for i, zone in enumerate(zones):
        result[zone] = people[(i + offset) % len(people)]
    return result

def render_schedule_text():
    sched = get_schedule_for_today()
    lines = ["🧹 Расписание уборки на неделю:",
             f"📅 Неделя, стартовавшая {BASE_DATE.strftime('%d.%m.%Y')}"]
    for zone, person in sched.items():
        lines.append(f"▪ {zone}: {person}")
    return "\n".join(lines)

# — Обработчик команды /schedule
async def schedule_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(render_schedule_text())

# — Авто-отправка каждую неделю (понедельник, 09:00)
async def send_weekly(app):
    await app.bot.send_message(chat_id=CHAT_ID, text=render_schedule_text())

async def main():
    # инициализируем бота
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("schedule", schedule_command))

    # планировщик
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_weekly,
        trigger="cron",
        day_of_week="mon",
        hour=9,
        minute=0,
        args=[app],
    )
    scheduler.start()

    logging.info("Бот запущен, жду команду /schedule или понедельник 09:00")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

