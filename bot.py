import telebot
import yfinance as yf
import time
import os
import random

# 🛡️ Token și canal ID din variabile de mediu (pentru cloud)
TOKEN = os.getenv("TELEGRAM_TOKEN")
CANAL_ID = int(os.getenv("CANAL_ID"))

bot = telebot.TeleBot(TOKEN)

# 📊 Activul analizat
ACTIV = 'EURUSD=X'  # Cod Yahoo Finance pentru EUR/USD

def genereaza_semnal():
    try:
        data = yf.download(tickers=ACTIV, period="1d", interval="1m")
        if data.empty:
            return None

        last_price = data['Close'][-1]
        prev_price = data['Close'][-2]

        directie = "UP" if last_price > prev_price else "DOWN"
        expirare = random.choice([1, 2, 3])
        return f"EUR/USD {directie} {expirare}m"
    except:
        return None

def trimite_semnale():
    while True:
        semnal = genereaza_semnal()
        if semnal:
            bot.send_message(CANAL_ID, semnal)
            print(f"📤 Semnal trimis: {semnal}")
        else:
            print("⚠️ Eroare la generarea semnalului.")
        time.sleep(300)  # Așteaptă 5 minute

# ▶️ Pornim automat
trimite_semnale()
