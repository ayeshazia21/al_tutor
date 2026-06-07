import sqlite3

DB_NAME = "agent_memory.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_message(role, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO messages(role, content)
    VALUES (?, ?)
    """, (role, content))

    conn.commit()
    conn.close()


def load_messages(limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT role, content
    FROM messages
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    rows.reverse()

    return [
        {
            "role": row[0],
            "content": row[1]
        }
        for row in rows
    ]