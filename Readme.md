# 📅 Event Calendar Telegram Bot

A Telegram bot built using Python that allows users to manage their personal event calendar. Events are stored in a local SQLite database and users can add, edit, view, delete events and log meeting minutes easily via chat commands.

## ✅ Features

- Add, edit, delete events
- View upcoming events
- Log minutes of meetings
- View user profile & last login
- Local database with SQLite
- Fully asynchronous using `python-telegram-bot`

## ⚙️ Tech Stack

- Python 3.11.5
- python-telegram-bot v20.7
- SQLite (local database, (for event storage))
- asyncio (for asynchronous handling

## 🔧 Setup Instructions

1. Clone or download this repo



2. Create virtual environment:
  
   python -m venv venv
   venv\Scripts\activate  # Windows
            OR
   source venv/bin/activate  # For macOS/Linux

3. Install Dependencies

   pip install -r requirements.txt

4. Set Your Bot Token

   BOT_TOKEN=your_telegram_bot_token
   (   Make sure you have a valid Telegram Bot Token.)

5. Run the Bot

   python bot.py

   You'll see a message like:
   ✅ Bot is running...


#  🚪 Bot Commands


Command                                      Description

/start                                       Register and start the bot

/help                                        Show help and available commands

/addevent                                    Add a new calendar event

/editevent                                   Edit an existing event

/deleteevent                                 Delete an event

/viewevents                                  View upcoming events

/logminutes                                  Log minutes for a meeting

/profile                                     View your profile & upcoming events

# 📆 Database Design

1. Users Table

   user_id

   username

   last_login

2. Events Table

   event_id

   user_id

   title

   description

   date

   time

   notes

   Notes

# 📌 Notes

    This bot does not use cloud storage; everything is stored locally.

    Make sure to back up your SQLite database if needed.

    Ensure your machine stays on for the bot to stay active 


# 🚀 Future Enhancements

Google Calendar sync

Reminders and notifications

Share events with other users

PDF/CSV export of meeting logs


# 🔗 Links

SQLite Tutorial



# Made using Python & Telegram.