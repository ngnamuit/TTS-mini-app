import os
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.tts_engine import text_to_speech_gtts, text_to_speech_google

# init app
app = FastAPI()

# middleware avoid cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# init frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# mkdir output
OUTPUT_DIR = "output_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("frontend/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/text-to-speech/")
async def text_to_speech(text: str = Form(...), engine: str = Form("pyttsx3")):
    """
    API to convert text to speech.
    Parameters:
    - text: The text to be converted.
    - engine: The Text-to-Speech engine ("gtts" or "google").
    """
    if engine in ["pyttsx3", "gtts"]:
        file_path = text_to_speech_gtts(text, OUTPUT_DIR)
    elif engine == "google":
        file_path = text_to_speech_google(text, OUTPUT_DIR)
    else:
        return {"error": "Engine not supported"}
    return FileResponse(file_path, media_type="audio/mpeg", filename=os.path.basename(file_path))
