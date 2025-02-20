import sqlite3

def initialize_database():
    conn = sqlite3.connect("stocks.db")
    c = conn.cursor()
    
    # Create the tracked_stocks table if it does not exist
    c.execute("""
    CREATE TABLE IF NOT EXISTS tracked_stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT UNIQUE NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
