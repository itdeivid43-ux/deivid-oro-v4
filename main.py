import os
import threading
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot ORO V12.1 Activo - T1 T2 T3 - Deivid - OK"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Inicia Flask siempre
threading.Thread(target=run_flask, daemon=True).start()

# Intenta iniciar el bot solo si hay token
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if BOT_TOKEN:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔥 ORO V12.1 Activo T1 T2 T3 - Deivid")

    def run_bot():
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.run_polling()

    run_bot()
else:
    print("BOT_TOKEN no encontrado, solo Flask activo")
    # Mantiene Flask vivo
    import time
    while True:
        time.sleep(3600)
