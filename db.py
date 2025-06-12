import sqlite3
import os
import re

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

def extract_referenced_images():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    cursor.execute("SELECT message FROM messages")
    rows = cursor.fetchall()
    conn.close()

    pattern = r"\[Image\] .*?/uploads/([a-zA-Z0-9_\-]+\.(?:png|jpg|jpeg|gif))"
    referenced = set()

    for (content,) in rows:
        matches = re.findall(pattern, content)
        referenced.update(matches)

    return referenced


def cleanup_orphaned_images(upload_dir, referenced_files):
    removed = []
    for fname in os.listdir(upload_dir):
        if fname not in referenced_files:
            full_path = os.path.join(upload_dir, fname)
            if os.path.isfile(full_path):
                os.remove(full_path)
                removed.append(fname)
    return removed

def clear_images(upload_dir):
    for file in os.listdir(upload_dir):
        os.remove(os.path.join(upload_dir, file))

def delete_last_message_by_username(username):
    db_path = "messages.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the ID of the most recent message by this user
    cursor.execute("""
        SELECT id FROM messages
        WHERE username = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (username,))
    row = cursor.fetchone()

    if row:
        message_id = row[0]
        cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        conn.commit()
        conn.close()
        return True  # success
    else:
        conn.close()
        return False  # no message found
