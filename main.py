import os, requests, time, threading
from flask import Flask
from datetime import datetime
import pytz
app=Flask(__name__)
@app.route('/')
def h(): return "ORO FEROZ V12 SOLO ORO"
TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
CHAT=os.getenv("TELEGRAM_CHAT_ID")
KEY=os.getenv("TWELVEDATA_API_KEY")
EC=pytz.timezone("America/Guayaquil")
def send(t):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":CHAT,"text":t})
def get():
    try:
        r=requests.get(f"https://api.twelvedata.com/stoch?symbol=XAU/USD&interval=5min&apikey={KEY}&k_period=13&d_period=3&slowing=3",timeout=10).json()
        return float(r['values'][0]['k']), float(r['values'][0]['d'])
    except: return None,None
def loop():
    time.sleep(5)
    send("✅ BOT ORO FEROZ V12 CONECTADO\n💛 SOLO XAU/USD\n📊 13,3,3 - 35/65\n🔥 FEROZ ACTIVO")
    while True:
        k,d=get()
        if k:
            hora=datetime.now(EC).strftime("%H:%M")
            if k<35 and d<40 and k>d: send(f"🟢 COMPRA ORO FEROZ 5M\n💛 XAU/USD\n⏰ {hora} EC\n📊 {k:.1f}/{d:.1f}")
            elif k>65 and d>60 and k<d: send(f"🔴 VENTA ORO FEROZ 5M\n💛 XAU/USD\n⏰ {hora} EC\n📊 {k:.1f}/{d:.1f}")
        time.sleep(300)
threading.Thread(target=loop,daemon=True).start()
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
