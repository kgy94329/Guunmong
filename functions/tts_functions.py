import base64
import datetime
import os
import requests
from elevenlabs import ElevenLabs
from elevenlabs import save
from dotenv import load_dotenv
import time

load_dotenv()

TTS_API_KEY = os.getenv('elevenlabs_api')

elevenlabs = ElevenLabs(
    api_key = TTS_API_KEY
)

def create_voice(text):
    print(f'[음성 합성 작업시작] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    audio_low_data = elevenlabs.text_to_speech.convert(
        voice_id="uyVNoMrnUku1dZyVEXwD",
        output_format="mp3_44100_128",
        text= text,
        model_id="eleven_multilingual_v2",
    )
    audio = base64.b64encode(b''.join(audio_low_data)).decode()
    print(f'[음성 합성 작업종료] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    return audio