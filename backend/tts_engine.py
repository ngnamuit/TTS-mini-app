import pyttsx3
import os
from gtts import gTTS
from google.cloud import texttospeech


def text_to_speech_gtts(text, output_dir):
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "output_gtts.mp3")

    tts = gTTS(text=text, lang="vi")
    tts.save(file_path)

    print(f"File đã được lưu tại: {file_path}")
    return file_path

def text_to_speech_google(text, output_dir):
    """
    Chuyển văn bản thành giọng nói bằng Google Text-to-Speech API (online).
    """
    file_path = os.path.join(output_dir, "output_google.mp3")
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="vi-VN", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(file_path, "wb") as out:
        out.write(response.audio_content)
    return file_path
