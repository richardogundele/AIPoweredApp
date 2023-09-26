import sqlite3, json
from fastapi import HTTPException

# Connect to the SQLite database
<<<<<<< HEAD
conn = sqlite3.connect("chats.db")
cursor = conn.cursor()

# Create the chat_history table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chathistory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        prompt TEXT,
        completion TEXT
    )
""")

def export_chat_data_to_jsonl():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("chats.db")
        cursor = conn.cursor()

        # Execute a SQL query to retrieve the chat data
        cursor.execute("SELECT user_email, prompt, completion FROM chathistory")
=======
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

def export_chat_data_to_jsonl():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("chat_app.db")
        cursor = conn.cursor()

        # Execute a SQL query to retrieve the chat data
        cursor.execute("SELECT user_email, text_input AS prompt, message AS result FROM chat_history")
>>>>>>> dc4bc8822be4c749ebcbc28f866dc9edac44039a

        # Fetch all rows of data
        chat_data = cursor.fetchall()

<<<<<<< HEAD
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
=======
        # Initialize a list to store chat messages
        chat_messages = []

        # Loop through the chat data and format it as chat messages
        for row in chat_data:
            user_message = {"role": "user", "content": row[1]}  # Extract prompt
            assistant_message = {"role": "assistant", "content": row[2]}  # Extract result
            system_message = {"role": "system", "content": character}

            chat_messages.extend([system_message, user_message, assistant_message])

        # Create a dictionary with the "messages" key
        chat_output = {"messages": chat_messages}

        # Define the name of the JSONL file
        jsonl_filename = "chat_data.jsonl"

        # Write the chat messages to a JSONL file
        with open(jsonl_filename, "w") as jsonl_file:
            json.dump(chat_output, jsonl_file, indent=4)

        # Close the database connection
        conn.close()

        return {"message": "Data exported to JSONL successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

>>>>>>> dc4bc8822be4c749ebcbc28f866dc9edac44039a
