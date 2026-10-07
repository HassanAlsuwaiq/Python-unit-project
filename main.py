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
    "Japanese":("JA","ja"),
    "Italian": ("IT","it"),
    "Bulgarian": ("BE","bg"),
    "Greek": ("EL","el"),
    "Indonesian":("ID","id"),
    "Dutch": ("NL","nl"),
    "Russian":("RU","ru"),
    "Turkish": ("TR","tr"),
    "Czech": ("CS","cs"),
    "Hindi": ("HI","hi"),
    "Polish": ("PL","pl"),
    "Slovak": ("Sk","sk"),
    "Ukrainian": ("UK","uk"),
    "Danish": ("DA","da"),
    "Estonian": ("ET","et"),
    "Croatian": ("HR","hr"),
    "Lithuanian": ("LT","lt"),
    "Slovenian": ("SL","sl"),
    "Vietnamese": ("VI","vi"),
    "German": ("DE","de"),
    "Finnish": ("FI","fi"),
    "Hungarian": ("HU","hu"),
    "Latvian": ("LV","lv"),
    "Romanian": ("RO","ro"),
    "Swedish": ("SV","sv")
                }

# Initialize the API clients with the respective API keys from environment variables
stt = SpeechToText(os.getenv("GROQ_API_KEY"))
gemini = GeminiProcessor(os.getenv("GEMINI_API_KEY"))
translator = Translator(os.getenv("DEEPL_API_KEY"))
tts = TextToSpeech()

# Function to process the audio file and perform speech-to-text, Gemini processing, translation, and text-to-speech
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
