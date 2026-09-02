import os, requests, time, threading
from flask import Flask
from datetime import datetime
import pytz

app = Flask(__name__)
@app.route('/')
def home(): return "BOT ORO SOLO ORO VIVO"

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")
API_KEY = os.getenv("TWELVEDATA_API_KEY")
EC = pytz.timezone("America/Guayaquil")

def send(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT, "text": text}, timeout=10)
        print("ENVIADO OK")
    except Exception as e:
        print(f"Error telegram: {e}")

def get_stoch_oro():
    try:
        url = f"https://api.twelvedata.com/stoch?symbol=XAU/USD&interval=5min&apikey={API_KEY}&k_period=13&d_period=3&slowing=3"
        r = requests.get(url, timeout=15).json()
        k = float(r['values'][0]['k'])
        d = float(r['values'][0]['d'])
        print(f"ORO Stoch: {k:.2f}/{d:.2f}")
        return k, d
    except Exception as e:
        print(f"Error stoch oro: {e}")
        return None, None

def bot_loop():
    time.sleep(5)
    send("✅ BOT ORO SOLO ORO CONECTADO\nXAU/USD 13,3,3 35/65 BINARIAS 5M\nYa estoy analizando ORO cada 5 min")
    while True:
        try:
            ahora = datetime.now(EC)
            if 6 <= ahora.hour <= 22:
                k, d = get_stoch_oro()
                if k is not None:
                    hora = ahora.strftime("%H:%M")
                    if k < 35 and d < 40 and k > d:
                        send(f"🟢 COMPRA ORO 5M\n💱 XAU/USD SOLO ORO\n⏰ {hora} EC\n📊 Stoch {k:.1f}/{d:.1f}\n✅ Cruce 35/65\n👉 Siguiente vela 5M")
                    elif k > 65 and d > 60 and k < d:
                        send(f"🔴 VENTA ORO 5M\n💱 XAU/USD SOLO ORO\n⏰ {hora} EC\n📊 Stoch {k:.1f}/{d:.1f}\n✅ Cruce 35/65\n👉 Siguiente vela 5M")
            time.sleep(300)
        except Exception as e:
            print(f"Error loop: {e}")
            time.sleep(10)

threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
