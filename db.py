import sqlite3
from datetime import datetime

DB_NAME = "event_calendar.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            last_login TEXT
        )
    ''')

    # Create events table
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            description TEXT,
            date TEXT,
            time TEXT,
            notes TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_or_update_user(user_id, username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if c.fetchone():
        c.execute("UPDATE users SET last_login = ? WHERE user_id = ?", (now, user_id))
    else:
        c.execute("INSERT INTO users (user_id, username, last_login) VALUES (?, ?, ?)",
                  (user_id, username, now))

    conn.commit()
    conn.close()
    
def get_user_profile(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Get user info
    c.execute("SELECT username, last_login FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()

    # Count events
    c.execute("SELECT COUNT(*) FROM events WHERE user_id = ?", (user_id,))
    event_count = c.fetchone()[0]

    conn.close()
    return user, event_count


def add_event(user_id, title, description, date, time, notes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (user_id, title, description, date, time, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, title, description, date, time, notes))
    conn.commit()
    conn.close()

    
def get_events(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT title, description, date, time, notes
        FROM events
        WHERE user_id = ?
        ORDER BY date, time
    ''', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_events_with_ids(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT event_id, title, description, date, time, notes
        FROM events
        WHERE user_id = ?
        ORDER BY date, time
    ''', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def update_event_field(event_id, field, new_value):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    query = f"UPDATE events SET {field} = ? WHERE event_id = ?"
    c.execute(query, (new_value, event_id))
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
    conn.commit()
    conn.close()


def update_event_field(event_id, field, new_value):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    query = f"UPDATE events SET {field} = ? WHERE event_id = ?"
    c.execute(query, (new_value, event_id))
    conn.commit()
    conn.close()

def get_user_profile(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Get user info
    c.execute("SELECT username, last_login FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()

    # Count events
    c.execute("SELECT COUNT(*) FROM events WHERE user_id = ?", (user_id,))
    event_count = c.fetchone()[0]

    conn.close()
    return user, event_count

def get_upcoming_events(user_id, limit=3):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT title, date, time FROM events 
        WHERE user_id = ? 
        ORDER BY date ASC, time ASC 
        LIMIT ?
    """, (user_id, limit))

    events = c.fetchall()
    conn.close()
    return events
