import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- 1. SERVIDOR WEB PARA RENDER (Esto arregla tu error) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ORO V12.1 Activo - T1 Breakout | T2 Reversion | T3 Hibrido - Deivid"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. TU BOT DE TELEGRAM ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Pon tu token en Render > Environment

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 **ORO V12.1 - DEIVID** 🔥\n\n"
        "✅ Bot Activo 24/7\n\n"
        "📊 Sistemas:\n"
        "T1 - Breakout\n"
        "T2 - Reversión\n"
        "T3 - Híbrido\n\n"
        "Usa /senales para ver el mercado"
    )

async def senales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Analizando ORO (XAUUSD) con T1, T2 y T3...")

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("senales", senales))
    application.run_polling()

if __name__ == "__main__":
    # Inicia Flask en un hilo aparte
    threading.Thread(target=run_flask, daemon=True).start()
    # Inicia el Bot
    run_bot()
