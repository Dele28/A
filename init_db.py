import sqlite3

DB_FILE = "stocks.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
