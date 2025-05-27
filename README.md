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

## 🚪 Bot Commands

/start - Welcome message

/help - Provides list of available commands

/addevent - Add a new event

/viewevents - View all upcoming events

/deleteevent - Delete a specific event

/editevent - Modify an event's details

/logminutes - Adds notes or minutes to meeting

/profile -Provides user ID, last login, total events and list of upcoming events


## 📆 Database Design

**Users Table**

1. user_id

2. username

3. last_login

 **Events Table**

1. event_id

2. user_id

3. title

4. description

5. date

6. time

7. notes

## 🚀 Future Enhancements

1. Google Calendar sync 

2. Reminders and notifications

3. Share events with other users

4. PDF/CSV export of meeting logs

## 📁 Project Structure

   ```text
   event_calendar_bot/
   ├── __pycache__/                  # Compiled Python bytecode (auto-generated)
   ├── venv/                         # Python virtual environment
   │   ├── Include/
   │   ├── Lib/
   │   ├── Scripts/
   │   └── pyvenv.cfg
   ├── bot.py                        # Main Telegram bot logic and command handling
   ├── db.py                         # SQLite database connection and queries
   ├── event_calendar.db             # SQLite database file storing event data
   ├── requirements.txt              # Python dependencies
   └── README.md                     # Project overview and setup  instructions
```

## 👤 Author

- Risa Fernandes
- GitHub: Risa-Fernandes
