import os
from dotenv import load_dotenv
from translatorAndGemini import GeminiProcessor, Translator
from text_to_speech import TextToSpeech
from speech_to_text import SpeechToText


load_dotenv()  # Load environment variables from .env file


# language name -> (DeepL code, TTS code)
LANGUAGES = {
    "English": ("EN-US", "en"),
    "French": ("FR", "fr"),
    "Spanish": ("ES", "es"),
    "Portuguese": ("PT-BR", "pt"),
    "Korean": ("KO", "ko"),
}

# loaded once, when this file is first imported


# Groq-hosted Whisper speech-to-text (from speech_to_text.py), needs GROQ_API_KEY in .env
stt = SpeechToText(os.getenv("GROQ_API_KEY"))
gemini = GeminiProcessor(os.getenv("GEMINI_API_KEY"))
translator = Translator(os.getenv("DEEPL_API_KEY"))
tts = TextToSpeech()


def process(audio_path, language):
    deepl_code, tts_code = LANGUAGES[language]

    text = stt.transcribe(audio_path)                  # speech -> Arabic text
    msa = gemini.process_text(text)

    translation = translator.translate(msa, deepl_code)

    wav = tts.synthesize(translation, tts_code)

    if wav is not None:
        tts.tts.save_audio(wav, "output.wav")
        return text, msa, translation, "output.wav"
    return text, msa, translation, None
