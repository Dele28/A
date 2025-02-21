import sqlite3

# Connect to your SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('stocks.db')
c = conn.cursor()

# Create the tracked_stocks table
c.execute('''
CREATE TABLE IF NOT EXISTS tracked_stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT UNIQUE NOT NULL
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database setup complete! Table 'tracked_stocks' created.")
