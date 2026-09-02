import os, requests, time
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")

def send(t):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT, "text": t}, timeout=10)
    except: pass

send("✅ ORO V4 CONECTADO - Prueba sin pandas")

while True:
    time.sleep(60)
