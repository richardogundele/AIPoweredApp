import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("chat_app.db")
cursor = conn.cursor()

# Create the chat_history table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        text_input TEXT,
        message TEXT
    )
""")

# Commit the changes and close the database connection
conn.commit()
conn.close()
