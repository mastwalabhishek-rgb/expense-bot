
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from datetime import datetime
import json, os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DATA_FILE = "data.json"

# ---------------- DATA ----------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ---------------- HANDLER ----------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.strip()

    hindi_numbers = {
        "एक":1,"दो":2,"तीन":3,"चार":4,"पांच":5,
        "छह":6,"सात":7,"आठ":8,"नौ":9,"दस":10
    }

    if "खर्च" in text:
        data = load_data()
        month = datetime.now().strftime("%Y-%m")
        total = sum(e["amount"] for e in data if e["date"].startswith(month))
        await update.message.reply_text(f"इस महीने का कुल खर्च ₹{total}")
        return

    words = text.split()
    qty = hindi_numbers.get(words[0], 1)
    item = " ".join(words[1:])

    prices = {"चाय":10,"कॉफी":20,"पेट्रोल":100}
    amount = qty * prices.get(item, 0)

    data = load_data()
    data.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "item": item,
        "amount": amount
    })
    save_data(data)

    await update.message.reply_text(f"₹{amount} save हो गया")

# ---------------- MAIN ----------------

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()


