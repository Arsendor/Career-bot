import sqlite3
import json
from config import DATABASE

conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

# Создание таблиц
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    age TEXT,
    education TEXT,
    interests TEXT,
    skills TEXT,
    profile TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    user_message TEXT,
    bot_response TEXT,
    timestamp TEXT
)
""")

conn.commit()

# Загрузка профессий из JSON (для демонстрации)
with open("c:/my_python/Final_Project/professions.json", encoding="utf-8") as f:
    professions = json.load(f)

cur.execute("DROP TABLE IF EXISTS professions_demo")
cur.execute("""
CREATE TABLE professions_demo (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    interests TEXT,
    level TEXT,
    link TEXT
)
""")

for p in professions:
    interests_str = ",".join(p["interests"])
    cur.execute("""
    INSERT INTO professions_demo (id, title, description, interests, level, link)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (p["id"], p["title"], p["description"], interests_str, p["level"], p["link"]))

conn.commit()
conn.close()

def init_db():
    """Инициализация базы данных."""
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        age TEXT,
        education TEXT,
        interests TEXT,
        skills TEXT,
        profile TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_message TEXT,
        bot_response TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_user_profile(telegram_id, age, education, interests, skills, profile):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO users (telegram_id, age, education, interests, skills, profile)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (telegram_id, age, education, interests, skills, profile))

    conn.commit()
    conn.close()


def save_conversation(user_id, user_message, bot_response, timestamp):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO conversations (user_id, user_message, bot_response, timestamp)
    VALUES (?, ?, ?, ?)
    """, (user_id, user_message, bot_response, timestamp))

    conn.commit()
    conn.close()


# --- первоначальная загрузка профессий ---
conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

with open("c:/my_python/Final_Project/professions.json", encoding="utf-8") as f:
    professions = json.load(f)

cur.execute("DROP TABLE IF EXISTS professions_demo")
cur.execute("""
CREATE TABLE professions_demo (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    interests TEXT,
    level TEXT,
    link TEXT
)
""")

for p in professions:
    interests_str = ",".join(p["interests"])
    cur.execute("""
    INSERT INTO professions_demo (id, title, description, interests, level, link)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (p["id"], p["title"], p["description"], interests_str, p["level"], p["link"]))

conn.commit()
conn.close()

print("База данных и таблицы созданы. Профессии загружены.")