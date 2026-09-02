import os
import asyncio
from telegram.ext import Application, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

# TU CODIGO DE ANALISIS AQUI - DEJA TU FUNCION analizar
# Ejemplo:
async def analizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Analizando oro V13... T1 T2 T3")

TOKEN = os.getenv("TELEGRAM_TOKEN")

application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("analizar", analizar))
application.add_handler(CommandHandler("oro", analizar))
application.add_handler(CommandHandler("start", analizar))

async def main():
    await application.bot.delete_webhook(drop_pending_updates=True)
    print("Webhook borrado, iniciando polling...")
    await application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
