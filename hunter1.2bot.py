import time
import requests
from binance.client import Client
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import matplotlib.pyplot as plt
import io
from datetime import datetime

# Binance API keys
BINANCE_API_KEY = "YOUR_BINANCE_API_KEY"
BINANCE_SECRET_KEY = "YOUR_BINANCE_SECRET_KEY"

# Telegram bot details
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

# Initialize Binance client
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

# Initialize Telegram bot
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

is_running = False

async def send_telegram_alert(image):
    """Send an alert image to Telegram."""
    await app.bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image)

def get_price(symbol):
    """Fetch the latest price from Binance."""
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker["price"])

def generate_price_image(price, symbol):
    """Generate an image of the current price with the time zone (UTC)."""
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, f"{symbol} Price: ${price}\nTime (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
            horizontalalignment='center', verticalalignment='center', fontsize=15, transform=ax.transAxes)
    ax.axis('off')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_running
    is_running = True
    await update.message.reply_text("Bot started!")
    asyncio.create_task(price_check_loop())

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_running
    is_running = False
    await update.message.reply_text("Bot stopped!")

async def price_check_loop():
    """Loop to check price and send alerts."""
    while is_running:
        try:
            for symbol in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]:
                price = get_price(symbol)
                print(f"Current {symbol} price: ${price}")

                # Set your price condition to trigger the alert (e.g., BTC price >= 50,000)
                if (symbol == "BTCUSDT" and price >= 50000) or \
                   (symbol == "ETHUSDT" and price >= 4000) or \
                   (symbol == "SOLUSDT" and price >= 200):
                    image = generate_price_image(price, symbol)
                    await send_telegram_alert(image)

            # Check price every 60 seconds
            await asyncio.sleep(60)

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)  # Wait before retrying

if __name__ == "__main__": 
    app.add_handler(CommandHandler("run", start_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.run_polling()
