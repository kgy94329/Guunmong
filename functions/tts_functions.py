import os
import requests
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import time

load_dotenv()

TTS_API_KEY = os.getenv('elevenlabs_api')

elevenlabs = ElevenLabs(
    api_key = TTS_API_KEY
)

async def create_voice(text):
    # elevenlabs.text_to_speech.convert(
    #     voice_id="JBFqnCBsd6RMkjVDRZzb",
    #     output_format="mp3_44100_128",
    #     text= text,
    #     model_id="eleven_multilingual_v2",
    # )
    time.sleep(5)
    return