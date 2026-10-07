import requests

# a class to send text to Gemini API for processing and translation
class GeminiProcessor:

    def __init__(self, api_key):
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent"

        self.headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        }



# prompt to make Gemini understand the Saudi dialect
        self.prompt = """
You are an expert in Saudi Arabic dialects.

Understand the Saudi dialect text provided by the user.
Convert it into clear and natural Modern Standard Arabic.
Preserve the original meaning and context.
Do not translate it into another language.
Do not explain anything.
Return only the rewritten Arabic text.
The output must be more than 10 characters.
"""

    # method to process text using Gemini API
    def process_text(self, text):

        data = {
            "systemInstruction": {
                "parts": [
                    {
                        "text": self.prompt
                    }
                ]
            },

            "contents": [
                {
                    "parts": [
                        {
                            "text": text
                        }
                    ]
                }
            ]
        }
        # lambda function to check if the response status code is 200
        is_ok = lambda r: r.status_code == 200                       
        # retry mechanism to handle errors
        for attempt in range(3):                                     
            response = requests.post(self.url, headers=self.headers, json=data, timeout=30)
            if is_ok(response):
                break
            print(f"Attempt {attempt + 1} failed")                                      
        # if the response is successful, return the processed text
        if is_ok(response):
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        # if the response status code is 503, return the original text
        elif response.status_code == 503:
            print("Gemini is busy, using the original text.")
            return text
        # if the response status code is not 200 and not 503, print the error and return the original text
        else:
            print("Gemini error:", response.status_code)
            return text

# class to handle translation using DeepL API
class Translator:

    def __init__(self, api_key):
        self.url = "https://api-free.deepl.com/v2/translate"

        self.headers = {
            "Authorization": f"DeepL-Auth-Key {api_key}"
        }

    # method to translate text using DeepL API
    def translate(self, text, target_language):

        # target_language = normalize_language(target_language)

        data = {
            "text": [text],
            "target_lang": target_language
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json=data
        )

        if response.status_code == 200:

            translated_text = response.json()["translations"][0]["text"]

            return translated_text

        else:

            print("DeepL error:", response.status_code)

            return None