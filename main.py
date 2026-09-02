import os, requests, time
from datetime import datetime
import math

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")
API_KEY = os.getenv("TWELVE_API_KEY")

def send(t):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT, "text": t, "parse_mode": "HTML"}, timeout=10)
    except: pass

def get_xau():
    try:
        url = f"https://api.twelvedata.com/price?symbol=XAU/USD&apikey={API_KEY}"
        r = requests.get(url, timeout=10).json()
        return float(r['price'])
    except:
        return None

def get_indicators():
    try:
        # RSI y EMA de Twelve Data
        url = f"https://api.twelvedata.com/rsi?symbol=XAU/USD&interval=5min&apikey={API_KEY}"
        rsi = float(requests.get(url, timeout=10).json()['values'][0]['rsi'])

        url = f"https://api.twelvedata.com/ema?symbol=XAU/USD&interval=5min&time_period=20&apikey={API_KEY}"
        ema20 = float(requests.get(url, timeout=10).json()['values'][0]['ema'])

        price = get_xau()
        return price, rsi, ema20
    except:
        return None, None, None

send("✅ <b>BOT ORO XAUUSD FOREX V4 ACTIVO</b>\n💰 Par: XAUUSD\n⏰ Timeframe: 5M/15M\n🔍 Buscando entradas...")

while True:
    try:
        price, rsi, ema = get_indicators()
        if price and rsi and ema:
            hora = datetime.now().strftime("%H:%M:%S")
            # ESTRATEGIA ORO FOREX
            if rsi < 35 and price > ema:
                tp = price + 5
                sl = price - 3
                send(f"🟢 <b>COMPRA XAUUSD ORO</b>\n💰 Precio: {price}\n📊 RSI: {rsi:.1f} (Sobreventa)\n📈 EMA20: {ema:.2f}\n✅ <b>TP:</b> {tp:.2f} (+50 pips)\n❌ <b>SL:</b> {sl:.2f} (-30 pips)\n⏰ {hora}\n🔥 FOREX")
            elif rsi > 65 and price < ema:
                tp = price - 5
                sl = price + 3
                send(f"🔴 <b>VENTA XAUUSD ORO</b>\n💰 Precio: {price}\n📊 RSI: {rsi:.1f} (Sobrecompra)\n📉 EMA20: {ema:.2f}\n✅ <b>TP:</b> {tp:.2f} (-50 pips)\n❌ <b>SL:</b> {sl:.2f} (+30 pips)\n⏰ {hora}\n🔥 FOREX")

        time.sleep(180) # analiza cada 3 minutos
    except:
        time.sleep(60)
