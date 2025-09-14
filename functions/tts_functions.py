import base64
import datetime
import os
import requests
import time
import wave
import io
from pydub import AudioSegment

from abc import ABC, abstractmethod

from elevenlabs import ElevenLabs
from dotenv import load_dotenv

from google import genai
from google.genai import types

ELEVENLABS_VOCAL = {'Anna Kim': 'uyVNoMrnUku1dZyVEXwD'}

class TTSStrategy(ABC):
    @abstractmethod
    def create_voice(self, text, vocal):
        pass

class ElevenLabsTTS(TTSStrategy):
    def __init__(self, api_key, vocal):
        self.api_key = api_key
        self.vocal = ELEVENLABS_VOCAL[vocal]
        self.elevenlabs = ElevenLabs(
            api_key = api_key
        )

    def create_voice(self, text):
        print(f'[음성 합성 작업시작] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        # TTS 처리 요청
        audio_low_data = self.elevenlabs.text_to_speech.convert(
            voice_id=self.vocal,
            output_format="mp3_44100_128",
            text= text,
            model_id="eleven_multilingual_v2",
        )

        # 음성 데이터 처리
        audio = base64.b64encode(b''.join(audio_low_data)).decode()
        print(f'[음성 합성 작업종료] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        return audio

class GoogleTTS(TTSStrategy):
    def __init__(self, api_key, vocal):
        self.api_key = api_key
        self.vocal = vocal
        self.client = genai.Client(api_key=api_key)

    def create_voice(self, text):
        print(f'[음성 합성 작업시작] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        # TTS 처리 요청
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=self.vocal,
                        )
                    )
                ),
            )
        )

        # 음성데이터 처리
        audio = response.candidates[0].content.parts[0].inline_data.data
        audio_segment = AudioSegment(
            data=audio,
            sample_width=2,
            frame_rate=24000,
            channels=1
        )
        buffer = io.BytesIO()
        audio_segment.export(buffer, format="mp3")  # or "wav"
        b64_audio = base64.b64encode(buffer.getvalue()).decode("utf-8")
        print(f'[음성 합성 작업종료] {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        return b64_audio

class TTSSynthesizer:
    def __init__(self, strategy: TTSStrategy, vocal):
        self.strategy = strategy
        self.vocal = vocal

    def set_strategy(self, strategy: TTSStrategy):
        self.strategy = strategy

    def create_voice(self, text):
        return self.strategy.create_voice(text)
    
def get_synthesizer(model_name, vocal):
    load_dotenv()

    # user_choice = "google"  # 예: 사용자가 선택한 옵션
    if model_name == "Google":
        API_KEY = os.getenv('google_ai_studio_api')
        strategy = GoogleTTS(api_key=API_KEY, vocal=vocal)
    elif model_name == "ElevenLabs":
        API_KEY = os.getenv('elevenlabs_api')
        strategy = ElevenLabsTTS(api_key=API_KEY, vocal=vocal)
    else:
        raise ValueError("지원되지 않는 TTS 엔진")

    tts = TTSSynthesizer(strategy, vocal)
    return tts

if __name__ == "__main__":
    main()