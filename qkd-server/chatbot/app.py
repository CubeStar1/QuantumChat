from typing import List
from pathlib import Path
import os


import pydantic
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware


import google.generativeai as genai
from langchain_community.llms import Ollama



app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define message schema
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# Read API key
base_path = Path(__file__).parent
os.environ['GOOGLE_API_KEY'] = base_path.joinpath('gemini-api-key.txt').read_text().strip()

async def send_message_to_gemini(payload: dict):
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    payload = str(payload)
    # Generate the response from the model
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    response = model.generate_content([payload], safety_settings={'HATE_SPEECH': 'block_none'})

    # Extract the content from the response
    response_content = response.text
    # response_content = json.loads(response_content)


    return response_content

@app.post("/chat/")
async def chat(request: Request):
    try:
        # Get the JSON payload from the request
        payload = await request.json()

        # Call the Gemini API to get the response
        response_message = await send_message_to_gemini(payload)

        # Return the response message
        return {"response": response_message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))