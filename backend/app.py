import os
import time
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# import logging
# logging.basicConfig(level=logging.DEBUG)



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


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("frontend/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/text-to-speech/")
async def text_to_speech(text: str = Form(...), engine: str = Form("gtts"), speed: str = Form("1.0")):
    """
    API to convert text to speech.
    Parameters:
    - text: The text to be converted.
    - engine: The Text-to-Speech engine ("gtts").
    """
    if engine == "gtts":
        try:
            speed = float(speed)
            start_time = time.time()
            text_chunks = split_text_into_chunks(text, max_chars=500)
            with ThreadPoolExecutor() as executor:
                audio_results = list(executor.map(lambda chunk: process_chunk(chunk, speed), text_chunks))

            # Generator to stream audio to the client
            # region #TODO
            def audio_generator():
                for audio in audio_results:
                    yield audio

            print(f"[RUNTIME][GTTS Parallel] {time.time() - start_time} seconds, ---- speed {speed}")
            return StreamingResponse(audio_generator(), media_type="audio/mpeg")
            # endregion
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating TTS: {str(e)}")
    return {"error": "Engine not supported"}

def process_chunk(chunk, speed=1.0):
    tts = gTTS(text=chunk, lang="vi")
    audio_data = BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    if speed != 1.0:
        return adjust_audio(audio_data, speed)
    else:
        return audio_data.read()

def adjust_audio(audio_data, speed):
    # Load the audio into pydub
    audio = AudioSegment.from_file(audio_data, format="mp3")

    # Adjust speed using pydub
    if speed > 1.0:
        audio = audio.speedup(playback_speed=speed)
    else:
        # Slow down the audio
        audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * speed)})
        audio = audio.set_frame_rate(audio.frame_rate)

    # Export the modified audio to BytesIO
    output_audio = BytesIO()
    audio.export(output_audio, format="mp3")
    output_audio.seek(0)
    return output_audio.read()

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
