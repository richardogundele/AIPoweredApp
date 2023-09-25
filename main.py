from typing import Optional
from fastapi import FastAPI
app = FastAPI()


import openai, os, sqlite3
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai_gpt4 import text_to_text_response
from database import export_chat_data_to_jsonl

openai.api_key = os.getenv("OPENAI_API_KEY")

origins = [ 
           "https://localhost:5173",
           "hhtps://localhost:5174",
           "https://localhost:4173",
           "https://localhost:3000",
           ]

app.add_middleware( 
                   CORSMiddleware, 
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

@app.get("/")
def read_root():
    return {"ThespAIn": "/Welcome To ThespAIn Backend Code"}

#User registration endpoint       
@app.post("/getstarted")
async def get_started(email):
    conn = sqlite3.connect("chat_app.db")
    cursor = conn.cursor()
    # Check if the email already exists in the database
    cursor.execute("SELECT email FROM users WHERE email=?", (email,))
    existing_email = cursor.fetchone()
    
    if existing_email:
        # Email already exists, no need to insert it again
        conn.close()
        return {"message": "User signed in successfully"}
    else:
        # Email doesn't exist, so insert it as a new user
        cursor.execute("INSERT INTO users(email) VALUES (?)", (email,))
        conn.commit()
        conn.close()
        return {"message": "User registered successfully"}

@app.post("/text")
async def post_text(email, textinput):
    # Get the response from the OpenAI model
    message = text_to_text_response(textinput)
    # Save the conversation to the database
    conn = sqlite3.connect("chat_app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_email, text_input, message) VALUES (?, ?, ?)", (email, textinput, message))
    conn.commit()
    conn.close()
    print("text message posted successfully")
    return message

#get speech
@app.post("/speech")
async def post_speech(email, file:UploadFile= File(...)):
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_input)
    # text_decoded = convert_speech_to_text(audio_input)  
    text_decoded = transcript["text"]
    if not text_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode Audio")
    else:
        message = text_to_text_response(text_decoded)
    return message
    
#get history
@app.get("/history/{email}")
async def get_chat_history(email):
    conn = sqlite3.connect("chat_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT text_input, message FROM chat_history WHERE user_email=?", (email,))
    chat_history = [{"text_input": row[0], "message":row[1]} for row in cursor.fetchall()]
    conn.close()
    trigger_export()
    return {"chat_history":chat_history}
    
@app.post("/export_for_fine_tuning")
async def trigger_export():
    result = export_chat_data_to_jsonl()
    return result



# async def post_speech(speech_converted):
#     chat_response = text_to_text_response(speech_converted)
#     if not chat_response:
#         return HTTPException(status_code=400, details="Failure to get chat response")
#     return chat_response
    # audio_output = convert_text_to_speech(chat_response)
    # if not audio_output:
    #     return HTTPException(status_code=400, detail="failed to get audio")
    # def iterfile():
    #     yield audio_output
    # return StreamingResponse(iterfile(), media_type="application/octet-stream")
