import sqlite3, json, os, asyncpg
from fastapi import HTTPException


async def connect_to_database():
    db_url = os.getenv("DATABASE_URL")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    conn = await asyncpg.connect(db_url, user=db_user, password=db_password)
    return conn


def export_chat_data_to_jsonl():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("chats.db")
        cursor = conn.cursor()

        # Execute a SQL query to retrieve the chat data
        cursor.execute("SELECT user_email, prompt, completion FROM chathistory")

        # Fetch all rows of data
        chat_data = cursor.fetchall()

        # Define the name of the JSONL file
        jsonl_filename = "chat_data.json"

        # Open the JSONL file for writing
        with open(jsonl_filename, "w") as jsonl_file:
            # Loop through the chat data and format it as JSONL
            for row in chat_data:
                user_email, prompt, completion = row
                chat_entry = {
                    "user_email": user_email,
                    "prompt": prompt,
                    "completion": completion
                }
                # Write each chat entry as a JSON object on a separate line
                json.dump(chat_entry, jsonl_file)
                jsonl_file.write("\n")  # Add a newline to separate entries

        # Close the database connection
        conn.close()
        return {"message": "Data exported to JSONL successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
