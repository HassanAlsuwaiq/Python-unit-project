from supertonic import TTS
from IPython.display import Audio, display


class TextToSpeech:

    def __init__(self):
        # Load the Supertonic model
        self.tts = TTS(auto_download=True)

        # Load the voice style
        self.style = self.tts.get_voice_style(voice_name="M1")

    def synthesize(self, text, language):

        # Check that the input is text
        if not isinstance(text, str):
            return None

        # Text must contain at least 10 characters
        if len(text.strip()) < 10:
            return None

        # Generate speech
        wav, duration = self.tts.synthesize(
            text,
            voice_style=self.style,
            lang=language
        )

        return wav

    def play_audio(self, audio):

        self.tts.save_audio(audio, "output.wav")
        display(Audio("output.wav", autoplay=True))