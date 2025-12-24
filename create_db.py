import sqlite3
import os

# Get absolute path → ai-mock-interview/data/sessions.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "sessions.db")

# Create /data folder if it doesn’t exist
os.makedirs(DATA_DIR, exist_ok=True)

# Connect using absolute path
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    overall_score INTEGER,
    eye_contact INTEGER,
    emotion TEXT,
    confidence INTEGER,
    posture TEXT,
    distraction INTEGER,
    tips TEXT
)
""")

conn.commit()
conn.close()

print("✔ sessions.db created successfully at:", DB_PATH)
