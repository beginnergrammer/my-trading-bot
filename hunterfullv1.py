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
BINANCE_API_KEY = "xz1tDCN4Jm8XjLPtxJgLUXNV0jxK8B9f7qYnHLUb8J6qZESYQujfXGCUMQFC6Xwl"
BINANCE_SECRET_KEY = "3Jn7lVbRfwmub7F2k9mopDWwQbqKe6JgemUsdizMKphGbDAm03QYH0Yc9zwZasYO"

# Telegram bot details
TELEGRAM_BOT_TOKEN = "8139114377:AAHmCNqlb1znbEBlLR3MJSoCi1wnvHv6Tgw"
TELEGRAM_CHAT_ID = "5508533721"

# Initialize Binance client
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

# Initialize Telegram bot
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

async def send_telegram_alert(image):
    """Send an alert image to Telegram."""
    await app.bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image)

def get_price(symbol):
    """Fetch the latest price from Binance."""
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker["price"])

def get_previous_candle_close(symbol):
    """Fetch the closing price of the previous 15-minute candle."""
    candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE, limit=2)
    return float(candles[-2][4])  # Closing price of the second last candle

def generate_price_image(price, symbol, previous_close):
    """Generate an image of the current price with the time zone (UTC) and percentage change."""
    fig, ax = plt.subplots()
    color = "black"   
    change = 0
    
    if previous_close is not None:
        change = price - previous_close
        change_percent = (change / previous_close) * 100
        if change > 0:
            color = "green"
            change_text = f" (↑ {change:.2f}, {change_percent:.2f}%)"
        elif change < 0:
            color = "red"
            change_text = f" (↓ {change:.2f}, {change_percent:.2f}%)"
    
    ax.text(0.5, 0.5, f"{symbol} Price: ${price}\nChange: {change_text}\nTime (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
            horizontalalignment='center', verticalalignment='center', fontsize=15, color=color, transform=ax.transAxes)
    ax.axis('off')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
    """Handle the price commands."""
    price = get_price(symbol)
    previous_close = get_previous_candle_close(symbol)
    image = generate_price_image(price, symbol, previous_close)
    await send_telegram_alert(image)

async def pbtc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await price_command(update, context, "BTCUSDT")

async def peth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await price_command(update, context, "ETHUSDT")

async def psol_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await price_command(update, context, "SOLUSDT")

if __name__ == "__main__":
    app.add_handler(CommandHandler("pbtc", pbtc_command))
    app.add_handler(CommandHandler("peth", peth_command))
    app.add_handler(CommandHandler("psol", psol_command))
    app.run_polling()