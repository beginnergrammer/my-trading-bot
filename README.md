# Telegram Price Display Bot

## Overview

This bot fetches real-time cryptocurrency prices from Binance and sends updates to a Telegram chat. It generates a price chart and sends it as an image via Telegram commands.

## Features

- Supports BTC, ETH, and SOL prices
- Sends price updates as images
- Uses Binance API for real-time data
- Secure API key handling via environment variables

## Requirements

- Python 3.8+
- Binance API Key
- Telegram Bot Token
- A Telegram chat ID
- Required Python packages (see below)

## Installation

1. Clone the Repository
    ```sh
    git clone [https://github.com/your-repo/telegram-price-bot.git](https://github.com/beginnergrammer/my-trading-bot/blob/main/hunterfullv1.py)
    cd telegram-price-bot
    ```

2. Install Dependencies
    ```sh
    pip install -r requirements.txt
    ```

3. Set Up Environment Variables

    Create a `.env` file in the project directory and add:
    ```env
    BINANCE_API_KEY=your_binance_api_key
    BINANCE_SECRET_KEY=your_binance_secret_key
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    ```

4. Run the Bot
    ```sh
    python bot.py
    ```

## Usage

Use the following commands in your Telegram chat:
- `/pbtc` - Get Bitcoin price
- `/peth` - Get Ethereum price
- `/psol` - Get Solana price

## Deployment

For continuous running, use a cloud service like Heroku, AWS, or a VPS. You can also use `screen` or `tmux` to keep it running on a server.

## Notes

- Ensure your Telegram bot has permissions to send messages and images.
- Keep your API keys secure and do not share them.

## Support

For issues or improvements, contact [superslight903@example.com].
