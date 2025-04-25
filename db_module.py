# db_module.py

import sqlite3

DB_NAME = "kaiftourkz.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS clients (
        chat_id     INTEGER PRIMARY KEY,
        name        TEXT,
        country     TEXT,
        date_from   TEXT,
        date_to     TEXT,
        budget      INTEGER,
        adults      INTEGER,
        children    INTEGER,
        created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at  TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS messages (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id     INTEGER NOT NULL,
        role        TEXT NOT NULL,
        content     TEXT NOT NULL,
        timestamp   TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(chat_id) REFERENCES clients(chat_id)
    );
    """)
    conn.commit()
    conn.close()

def save_client(chat_id, name=None, country=None, date_from=None, date_to=None, budget=None, adults=None, children=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO clients (chat_id, name, country, date_from, date_to, budget, adults, children)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(chat_id) DO UPDATE SET
        name=excluded.name,
        country=excluded.country,
        date_from=excluded.date_from,
        date_to=excluded.date_to,
        budget=excluded.budget,
        adults=excluded.adults,
        children=excluded.children,
        updated_at=CURRENT_TIMESTAMP
    """, (chat_id, name, country, date_from, date_to, budget, adults, children))
    conn.commit()
    conn.close()

def save_message(chat_id, role, content):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO messages (chat_id, role, content)
    VALUES (?, ?, ?)
    """, (chat_id, role, content))
    conn.commit()
    conn.close()

