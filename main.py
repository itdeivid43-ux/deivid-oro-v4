import os, requests, time, threading
from flask import Flask
import pytz
from datetime import datetime
app = Flask(__name__)
@app.route('/')
def home(): return "ORO TEST VIVO"
TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
CHAT=os.getenv("TELEGRAM_CHAT_ID")
EC=pytz.timezone("America/Guayaquil")
def send(t):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":CHAT,"text":t})
def loop():
    time.sleep(10)
    send("✅ BOT ORO SOLO ORO CONECTADO - MODO PRUEBA\nTe mando señal de prueba en 60 segundos")
    time.sleep(60)
    send("🟢 COMPRA BINARIAS ORO 5M (PRUEBA)\n💱 XAU/USD SOLO ORO\n⏰ Prueba\n📊 Stoch 28.5/30.1\n✅ Si ves esto, el bot SÍ funciona\n👉 Esta es solo prueba, espera la real")
    while True:
        time.sleep(300)
        now=datetime.now(EC).strftime("%H:%M")
        send(f"⏳ Bot ORO vivo {now} - Esperando cruce 35/65 real...")
threading.Thread(target=loop,daemon=True).start()
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
