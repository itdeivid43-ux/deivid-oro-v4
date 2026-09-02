import os, requests, time, threading
from datetime import datetime
from flask import Flask
import pytz
app = Flask(__name__)
@app.route('/')
def home(): return "BOT ORO SOLO ORO VIVO"

TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID=os.getenv("TELEGRAM_CHAT_ID")
API_KEY=os.getenv("TWELVEDATA_API_KEY")
EC=pytz.timezone("America/Guayaquil")

def send(t):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":CHAT_ID,"text":t}, timeout=15)
    except: pass

def get_stoch():
    try:
        r=requests.get(f"https://api.twelvedata.com/stoch?symbol=XAU/USD&interval=5min&apikey={API_KEY}&k_period=13&d_period=3&slowing=3",timeout=12).json()
        return float(r['values'][0]['k']), float(r['values'][0]['d'])
    except: return None,None

def bot_loop():
    time.sleep(5)
    send("✅ BOT ORO SOLO ORO CONECTADO\nXAU/USD 13,3,3 35/65 - BINARIAS 5M")
    while True:
        try:
            ahora=datetime.now(EC); hora=ahora.strftime("%H:%M")
            if 6 <= ahora.hour <= 22:
                k,d=get_stoch()
                if k:
                    if k<35 and d<40 and k>d:
                        send(f"🟢 COMPRA BINARIAS ORO 5M\n💱 XAU/USD SOLO ORO\n⏰ {hora} EC\n📊 Stoch {k:.1f}/{d:.1f}\n👉 Siguiente vela 5M")
                    elif k>65 and d>60 and k<d:
                        send(f"🔴 VENTA BINARIAS ORO 5M\n💱 XAU/USD SOLO ORO\n⏰ {hora} EC\n📊 Stoch {k:.1f}/{d:.1f}\n👉 Siguiente vela 5M")
            time.sleep(300)
        except: time.sleep(10)

threading.Thread(target=bot_loop,daemon=True).start()
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
