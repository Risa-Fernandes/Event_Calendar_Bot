# Event Calendar Bot

A Telegram-based Event Calendar Bot that helps users manage and organize their personal events via chat commands. Built using Python, `python-telegram-bot`, and SQLite.

## 🚀 Features

- Add events with title, date, time, and optional description
- View upcoming events
- Edit or delete existing events
- Stores user data in a local SQLite database
- Easy-to-use conversational interface on Telegram

## 🛠️ Tech Stack

- **Python 3.10+**
- **python-telegram-bot** (Telegram Bot API)
- **SQLite** (for local event storage)

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/event_calendar_bot.git
   cd event_calendar_bot

2. **Set up a virtual environment**:
   ```bash
    python -m venv venv
    source venv/bin/activate     # On Windows use: venv\Scripts\activate
3. **Install dependencies**:
     ```bash
     pip install -r requirements.txt
4. **Set up your Telegram Bot token**:
     Create a .env file and add your token:
     ```ini
     TELEGRAM_TOKEN=your_telegram_bot_token_here
5. **Run the bot**:
     ```bash
     python bot.py
