from flask import Flask, request
import requests
import yfinance as yf
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_momentum(symbol):
    ticker = f"{symbol}=X" if not symbol.endswith("=X") else symbol
    data = yf.download(ticker, interval="1m", period="1d", progress=False)
    data['momentum'] = data['Close'] - data['Close'].shift(10)
    momentum = data['momentum'].iloc[-1].item()
    close = data['Close'].iloc[-1].item()
    signal = "BUY" if momentum > 0 else "SELL" if momentum < 0 else "NEUTRAL"
    return f"📈 {symbol} (1m)\nSignal: {signal}\nMomentum: {momentum:.5f}\nClose: {close:.5f}"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    if text.startswith("/check"):
        parts = text.split()
        if len(parts) == 2:
            symbol = parts[1].upper()
            try:
                msg = get_momentum(symbol)
            except Exception as e:
                msg = f"⚠️ Eroare la analiză: {e}"
        else:
            msg = "❗ Folosește comanda astfel: /check EURUSD"
    elif text == "/start":
        msg = "👋 Salut! Trimite /check EURUSD pentru semnal Momentum."
    elif text == "/help":
        msg = "📘 Comenzi disponibile:\n/check EURUSD – semnal Momentum\n/start – bun venit\n/help – ajutor"
    else:
        msg = "❓ Comandă necunoscută. Trimite /help."

    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": msg})
    return {"ok": True}

@app.route("/", methods=["GET"])
def home():
    return "Botul rulează! ✅"
