from typing import Optional
from fastapi import FastAPI
app = FastAPI()


import openai, os, sqlite3, random
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai_gpt4 import text_to_text_response, convert_text_to_speech
from database import *

openai.api_key = os.getenv("OPEN_AI_KEY")

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
users = {}

@app.get("/")
def read_root():
    return {"ThespAIn": "/itworking"}

#User registration endpoint       
@app.post("/register")
async def register_user(email):
    # email = user_data.email
    conn = sqlite3.connect("chat_app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(email) VALUES (?)", (email,))
    conn.commit()
    conn.close()
    return {"message":"User registered successfully"}

@app.post("/login")
async def login_user(email):
    # email = user_data.email
    conn = sqlite3.connect("chat_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email=?", (email,))
    user_id = cursor.fetchone()
    conn.close()
    if user_id:
        return {"message":"Login successful",}
    else:
        raise HTTPException(status_code=401, details="Authentication failed")

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

#get history
@app.get("/history/{email}")
async def get_chat_history(email):
    conn = sqlite3.connect("chat_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT text_input, message FROM chat_history WHERE user_email=?", (email,))
    chat_history = [{"text_input": row[0], "message":row[1]} for row in cursor.fetchall()]
    conn.close()
    
    return {"chat_history":chat_history}
#get speech
@app.post("/speech")
async def post_speech(speech_input: dict):
    email = speech_input.get("email")
    speech_converted = speech_input.get("speech_converted")
    if email in users:
        chat_response = "response"  # Replace with actual response
        users[email]["history"].update({speech_converted: chat_response})
        return {"message": "Speech message posted successfully"}
    else:
        return {"message": "User not found"}
    
# async def post_speech(file:UploadFile= File(...)):
#     with open(file.filename, "wb") as buffer:
#         buffer.write(file.file.read())
#     audio_input = open(file.filename, "rb")
#     text_decoded = convert_speech_to_text(audio_input)  
#     print(text_decoded)
#     if not text_decoded:
#         raise HTTPException(status_code=400, detail="Failed to decode Audio")
# async def post_speech(speech_converted):
    # chat_response = text_to_text_response(speech_converted)
    # print(chat_response)
    # if not chat_response:
    #     return HTTPException(status_code=400, details="Failure to get chat response")
    
    # audio_output = convert_text_to_speech(chat_response)
    # if not audio_output:
    #     return HTTPException(status_code=400, detail="failed to get audio")
    
    # def iterfile():
    #     yield audio_output
        
    # return StreamingResponse(iterfile(), media_type="application/octet-stream")


@app.post("/text_to_speech")
async def text_to_speech(covert):
    message = text_to_text_response(text_input=covert)

    audio_output = convert_text_to_speech(message)
    if not audio_output:
        return HTTPException(status_code=400, detail="failed to get audio")
    
    def iterfile():
        yield audio_output
        
    return StreamingResponse(iterfile(), media_type="application/octet-stream")