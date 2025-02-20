import sqlite3

def init_db():
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()

    with open("schema.sql", "r") as f:
        c.executescript(f.read())

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
