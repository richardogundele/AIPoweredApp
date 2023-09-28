#libraries
import openai, os
from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException

#functions used
from dbconnect import getSession
from apirequests import text_to_text_response
from dbfunctions import getChats, saveChat, check_and_add_email

app = FastAPI()   #fastAPI initialization

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

@app.on_event("startup")
def startup_db_client():
    app.state.db = getSession()

@app.on_event("shutdown")
def shutdown_db_client():
     app.state.db.close()

@app.get("/")
def read_root():
    return {"ThespAIn": "/Welcome To ThespAIn Backend Code"}

#User registration endpoint       
@app.post("/getstarted")
async def get_started(email):
    check_and_add_email(email=email)
    return ("Welcome")

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
        raise HTTPException(status_code=400, detail="Failed to decode Audio from Whisper")
    else:
        message = text_to_text_response(text_decoded)
    return message

@app.post("/text")
async def post_text(email, textinput):
    # Get the response from the OpenAI model
    message = text_to_text_response(textinput)
    #saved to database
    saved = saveChat(email=email, prompt=textinput, completion=message)
    print(f">>>>>>>>>>>> {saved}")
    # Save the conversation to the database
    print("database stored successfully")
    return message

#get history
@app.get("/history/{email}")
def get_chat_history(email):
    rs =  getChats(email)
    if (len(rs) <= 0):
           return{"chat_history":[]}
    # rs = json.dumps(rs)
    # trigger_export()
    return {"chat_history":rs}
    
# @app.post("/export_for_fine_tuning")
# async def trigger_export():
#     result = export_chat_data_to_jsonl()
#     return result
