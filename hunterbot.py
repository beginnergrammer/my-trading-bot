import time
import requests
from binance.client import Client
from telegram import Bot
from telegram.ext import Application

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

async def send_telegram_alert(message):
    """Send an alert message to Telegram."""
    await app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def get_price():
    """Fetch the latest price from Binance."""
    ticker = client.get_symbol_ticker(symbol="BTCUSDT")
    return float(ticker["price"])

async def main():
    """Main loop to check price and send alerts."""
    # Test message when bot starts
    await send_telegram_alert("Hello, your bot is up and running!")
    
    while True:
        try:
            price = get_price()
            print(f"Current BTC price: ${price}")

            # Set your price condition to trigger the alert (e.g., BTC price >= 50,000)
            if price >= 50000:
                await send_telegram_alert(f"🚀 BTC hit ${price}! Time to check the charts!")

            # Check price every ? seconds
            time.sleep(5)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)  # Wait before retrying

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
