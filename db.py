import sqlite3

def create_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (username TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_message(username, message):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, message))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("SELECT username, message, timestamp FROM messages")
    messages = c.fetchall()
    conn.close()
    return messages

def delete_last_message(username):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("DELETE FROM messages WHERE rowid = (SELECT max(rowid) FROM messages WHERE username = ?)", (username,))
    conn.commit()
    conn.close()