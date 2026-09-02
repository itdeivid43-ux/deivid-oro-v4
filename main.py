import os, time, requests
from datetime import datetime
import yfinance as yf
import pandas as pd

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

def get_gold_signal():
    try:
        data = yf.download("GC=F", period="5d", interval="5m", progress=False)
        if len(data) < 50:
            return None
        data['EMA9'] = data['Close'].ewm(span=9).mean()
        data['EMA21'] = data['Close'].ewm(span=21).mean()
        last = data.iloc[-1]
        prev = data.iloc[-2]
        price = float(last['Close'])
        if prev['EMA9'] < prev['EMA21'] and last['EMA9'] > last['EMA21']:
            return f"🟢 *COMPRA ORO*\nPrecio: {price:.2f}\nEMA 9 cruzó arriba de 21\nHora: {datetime.now().strftime('%H:%M')}"
        if prev['EMA9'] > prev['EMA21'] and last['EMA9'] < last['EMA21']:
            return f"🔴 *VENTA ORO*\nPrecio: {price:.2f}\nEMA 9 cruzó abajo de 21\nHora: {datetime.now().strftime('%H:%M')}"
    except Exception as e:
        print(f"Error: {e}")
    return None

send("✅ *DEIVID-ORO-V4 CONECTADO* ✅\nBot iniciado, esperando señal de ORO...")

while True:
    signal = get_gold_signal()
    if signal:
        send(signal)
    time.sleep(300)
