from pydub import AudioSegment
import requests
import os

API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def get_emotion(audio_file_wav):
    audio = AudioSegment.from_wav(audio_file_wav)
    audio.export("testme.flac",format = "flac")
    def query(filename):
        with open(filename, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        return response.json()
    output = query("sample1.flac")
    return output
