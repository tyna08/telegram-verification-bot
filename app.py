import json
import os
import requests
from flask import Flask, request

app = Flask(__name__)

# 🔐 Get your Telegram bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable.")

# ✅ Valid product codes
valid_codes = {
    "G7X2W9L": "Batch A01 - Verified Genuine",
    "G4PQ8MZ": "Batch A02 - Verified Genuine",
    "G9RT3NY": "Batch A03 - Verified Genuine",
    "G1AB5KL": "Batch A04 - Verified Genuine",
    "G5DE8CU": "Batch A05 - Verified Genuine",
    "G3ZM7XQ": "Batch A06 - Verified Genuine",
    "K2X4MDZ": "Batch A07 - Verified Genuine",
    "L8Q3NRB": "Batch A08 - Verified Genuine",
    "C6Y7TPL": "Batch A09 - Verified Genuine",
    "H5V2WQX": "Batch A10 - Verified Genuine"
}

# 📦 File to track scanned codes
SCAN_LOG = "scanned.json"

def load_scan_log() -> set[str]:
    if os.path.exists(SCAN_LOG):
        with open(SCAN_LOG, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_scan_log(seen: set[str]) -> None:
    with open(SCAN_LOG, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, indent=2)

seen_codes = load_scan_log()

# ✅ Telegram sender
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

# 🔁 Webhook route
@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    incoming = message.get("text", "").strip().upper()

    print(f"📨 Received: {incoming}")

    if not incoming:
        send_message(chat_id, "❗ Please send a valid product code.")
        return {"ok": True}

    if incoming in seen_codes:
        send_message(chat_id, "⚠️ Already verified. This code has been scanned before. Please contact support if unsure.")
    elif incoming in valid_codes:
        seen_codes.add(incoming)
        save_scan_log(seen_codes)
        send_message(chat_id, f"✅ AUTHENTIC: {valid_codes[incoming]}")
    else:
        send_message(chat_id, "❌ UNKNOWN: This product code is not recognised. Please check and try again. Possible counterfeit.")

    return {"ok": True}

# 🚀 Run Flask locally

@app.route("/", methods=["GET"])
def home():
    return "✅ Telegram Verification Bot is Running!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)



