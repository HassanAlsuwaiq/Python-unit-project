import requests


# a class to handle the conversion of speech to text using Groq API
class SpeechToText:
    def __init__(self, api_key):
        # check if the API key is provided
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing from .env")
        # if provided, set the API endpoint and headers for the request
        self.url = "https://api.groq.com/openai/v1/audio/transcriptions"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    # method to transcribe audio files
    def transcribe(self, audio_file):
        """
        Sends the audio file to Groq and returns the Arabic transcription.
        """
        with open(audio_file, "rb") as f:
            response = requests.post(
                self.url,
                headers=self.headers,
                files={"file": (audio_file, f, "audio/wav")},
                data={"model": "whisper-large-v3-turbo", "language": "ar"},
                timeout=60,
            )
        response.raise_for_status()
        return response.json()["text"].strip()
