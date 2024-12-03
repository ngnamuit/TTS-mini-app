import os
import time
from gtts import gTTS
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


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
    - engine: The Text-to-Speech engine ("gtts").
    """
    if engine == "gtts":
        try:
            start_time = time.time()
            text_chunks = split_text_into_chunks(text, max_chars=500)

            with ThreadPoolExecutor() as executor:
                audio_results = list(executor.map(process_chunk, text_chunks))

            print("[RUNTIME][GTTS Parallel] %s seconds ---" % (time.time() - start_time))
            # Generator to stream audio to the client
            def audio_generator():
                for audio in audio_results:
                    yield audio
            return StreamingResponse(audio_generator(), media_type="audio/mpeg")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating TTS: {str(e)}")
    return {"error": "Engine not supported"}

def process_chunk(chunk):
    tts = gTTS(text=chunk, lang="vi")
    audio_data = BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    return audio_data.read()

def split_text_into_chunks(text, max_chars=500):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
