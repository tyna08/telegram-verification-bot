import json
import os
import requests
from flask import Flask, request

app = Flask(__name__)

# 🔐 Get your Telegram bot token from an environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable.")


# ✅ Valid and fake product codes
valid_codes = {
    "G7X2W9L": "Batch A01 - Verified Genuine",
    "G4PQ8MZ": "Batch A02 - Verified Genuine",
    "G9RT3NY": "Batch A03 - Verified Genuine",
    "G1AB5KL": "Batch A04 - Verified Genuine",
    "G5DE8CU": "Batch A05 - Verified Genuine",
    "G3ZM7XQ": "Batch A06 - Verified Genuine",
    "J2T5P6K": "Batch A07 - Verified Genuine",
    "M7F4Y9D": "Batch A08 - Verified Genuine",
    "V3B2X1N": "Batch A09 - Verified Genuine",
    "Q9Z6L0W": "Batch A10 - Verified Genuine",

    "F1X0Y2A": "❌ FAKE",
    "Z8K3U7L": "❌ FAKE",
    "B9P2W6C": "❌ FAKE",
    "N0J8V4D": "❌ FAKE",
    "R3L7E1M": "❌ FAKE",
    "Y6H5X9Q": "❌ FAKE",
    "H4C2J8M": "❌ FAKE",
    "T2W5X9L": "❌ FAKE",
    "D7F6R2A": "❌ FAKE",
    "P1K9V0N": "❌ FAKE"
}

# 📁 Scan log for persistence
SCAN_LOG = "scanned.json"

def load_scan_log() -> set[str]:
    if os.path.exists(SCAN_LOG):
        with open(SCAN_LOG, "r", encoding="utf-8") as f:
            try:
                return set(json.load(f))
            except Exception:
                return set()
    return set()

def save_scan_log(seen: set[str]) -> None:
    with open(SCAN_LOG, "w", encoding="utf-8") as f:
        json.dump(sorted(seen), f, indent=2)

seen_codes = load_scan_log()

# ✅ Send message to user via Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{8128320823:AAHTjoC-CWHR6lALLnLeXgEY2jZtw1ovOBQ}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

# 🔁 Telegram webhook route
@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")

    if not chat_id:
        return {"ok": False, "error": "No chat ID"}

    incoming = message.get("text", "").strip().upper()
    print(f"📨 Received: {incoming}")

    if incoming not in valid_codes:
        send_message(chat_id, "❌ INVALID: This product code is not recognised.")
    elif incoming in seen_codes:
        send_message(chat_id, "⚠️ WARNING: This code has already been verified. Possible reuse.")
    else:
        seen_codes.add(incoming)
        save_scan_log(seen_codes)
        send_message(chat_id, f"✅ AUTHENTIC: {valid_codes[incoming]}")

    return {"ok": True}

# 🌐 Run app locally
@app.route("/", methods=["GET"])
def home():
    return "✅ Telegram Verification Bot is Running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


