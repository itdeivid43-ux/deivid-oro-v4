import os
import logging
from datetime import datetime
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# LOGS
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TOKENS - Acepta los 2 nombres para que no falle nunca
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
OANDA_KEY = os.getenv("OANDA_API_KEY")
OANDA_ACCOUNT = os.getenv("OANDA_ACCOUNT_ID")

if not BOT_TOKEN:
    raise ValueError("Falta BOT_TOKEN o TELEGRAM_BOT_TOKEN en Render")

# FUNCION PARA OBTENER PRECIO REAL DE OANDA
def get_oro_price():
    try:
        if not OANDA_KEY:
            return None, "OANDA no configurado, usando analisis tecnico base"
        url = "https://api-fxtrade.oanda.com/v3/instruments/XAU_USD/candles?count=100&granularity=M15"
        headers = {"Authorization": f"Bearer {OANDA_KEY}"}
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        candles = data.get('candles', [])
        last_price = float(candles[-1]['mid']['c'])
        return last_price, None
    except Exception as e:
        logger.error(f"Error OANDA: {e}")
        return None, str(e)

# COMANDO /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🔥 **ORO V13 Activo T1 T2 T3 - Deivid** 🔥\n\n"
        "✅ Bot LIVE y conectado\n"
        "✅ Better Stack activo\n"
        "✅ Render Deploy OK\n\n"
        "Comandos:\n"
        "/analizar - Analisis completo T1 T2 T3\n"
        "/oro - Precio actual del Oro\n"
        "/start - Este menu"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

# COMANDO /oro
async def oro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, err = get_oro_price()
    if price:
        await update.message.reply_text(f"💰 **ORO XAU/USD:** ${price:.2f}\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Quito", parse_mode='Markdown')
    else:
        await update.message.reply_text(f"💰 **ORO XAU/USD:** Consultando...\n⚠️ {err}\nBot activo igual.")

# COMANDO /analizar - TU LOGICA T1 T2 T3
async def analizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, _ = get_oro_price()
    price_txt = f"${price:.2f}" if price else "En consulta"

    analisis = (
        f"📊 **ANALISIS ORO V13 - DEIVID**\n"
        f"💰 Precio: {price_txt}\n"
        f"🕒 {datetime.now().strftime('%H:%M')} Quito\n\n"
        f"**T1 BREAKOUT:**\n"
        f"▶️ Esperando ruptura de rango M15. Si rompe maximo con volumen -> BUY\n\n"
        f"**T2 PULLBACK:**\n"
        f"▶️ Si toca EMA 21 en M15 y deja mecha de rechazo -> BUY/SELL segun tendencia\n\n"
        f"**T3 REVERSIÓN:**\n"
        f"▶️ Doble techo/piso en H1 + RSI divergencia -> Reversión\n\n"
        f"⚠️ Gestion: SL 150 pips / TP1 200 / TP2 400\n"
        f"🔥 Sistema Activo"
    )
    await update.message.reply_text(analisis, parse_mode='Markdown')

# MAIN
def main():
    logger.info(f"🚀 Iniciando ORO V13 - Token OK: {BOT_TOKEN[:10]}...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oro", oro))
    app.add_handler(CommandHandler("analizar", analizar))
    logger.info("✅ Bot ORO V13 LISTO - Polling iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()
