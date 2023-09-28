import requests, os, openai

openai.api_key = os.getenv("OPENAI_API_KEY")

ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

character = "You are a thespian with over 20 years experience in acting, script analysis, character development, colaboration, performance, character transformation, auditions and research."
def text_to_text_response(text_input):
    system = {"role": "system", "content": character}
    user = {"role":"user", "content":text_input}
    try:
        response = openai.ChatCompletion.create( model="gpt-4", max_tokens=500, temperature=0.1, messages= [system, user])
        result = response["choices"][0]["message"]["content"]
        
        return result 
    except Exception as e: 
        return ("Failed to get text response from GPT4 API")
        
# Eleven Labs -- Convert text to speech
def convert_text_to_speech(result):
  body = {
    "text": result,
    "voice_settings": {
        "stability": 0,
        "similarity_boost": 0
    }
  }
  voice_shaun = "mTSvIrm2hmcnOvb21nW2"
  voice_rachel = "21m00Tcm4TlvDq8ikWAM"
  voice_antoni = "ErXwobaYiN019PkySvjV"

  # Construct request headers and url
  headers = { "xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg" }
  endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

  try:
    response = requests.post(endpoint, json=body, headers=headers)
  except Exception as e:
     return

  if response.status_code == 200:
      # with open("output.wav", "wb") as f:
      #     f.write(audio_data)
      return response.content
  else:
    return
