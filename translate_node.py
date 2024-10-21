import torch
from io import BytesIO
import numpy as np
import requests

# Mapping language names to codes
names = ['Auto Detect','English','Albanian','Arabic','Azerbaijani','Bengali','Bulgarian','Catalan','Chinese','Chinese (traditional)',
        'Czech','Danish','Dutch','Esperanto','Estonian','Finnish','French','German','Greek','Hindi','Hungarian','Indonesian',
        'Irish','Italian','Japanese','Korean','Latvian','Lithuanian','Malay','Norwegian','Persian','Polish','Portuguese','Romanian',
        'Russian','Slovak','Slovenian','Spanish','Swedish','Tagalog','Thai','Turkish','Ukranian','Urdu']

codes = ['auto','en', 'sq', 'ar', 'az', 'bn', 'bg', 'ca', 'zh', 'zt', 'cs', 'da', 'nl', 'eo', 'et', 'fi', 'fr', 'de', 'el', 'hi', 'hu', 'id', 'ga', 'it',
         'ja', 'ko', 'lv', 'lt', 'ms', 'nb', 'fa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'es', 'sv', 'tl', 'th', 'tr', 'uk', 'ur']

# Mapping language names to codes
name_to_code = dict(zip(names, codes))

# Helper function to translate text locally
def translate_text_locally(text, source_code, target_code):
    url = "http://127.0.0.1:5000/translate"
    headers = {"Content-Type": "application/json"}
    data = {
        "q": text,
        "source": source_code,  
        "target": target_code,  
        "format": "text"
    }

    try:
        # Send the request with JSON payload and headers
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        translated_text = response_json.get('translatedText', "No translation found")
        return translated_text
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the translation server. Is the server running?"
    except requests.exceptions.Timeout:
        return "Error: The request to the translation server timed out."
    except requests.exceptions.RequestException as e:
        return f"Error: An error occurred while trying to connect to the translation server: {e}"

# Helper function to translate text online
def translate_text_online(text, source_code, target_code, api_key):
    url = "https://libretranslate.com/translate"
    headers = {"Content-Type": "application/json"}
    data = {
        "q": text,
        "source": source_code,
        "target": target_code,
        "format": "text",
        # Add API key only if it's not empty
        "api_key": api_key if api_key else None
    }

    try:
        # Send the request with JSON payload and headers
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Check if the response status is not an error
        response_json = response.json()
        translated_text = response_json.get('translatedText', "No translation found")
        return translated_text
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the translation server."
    except requests.exceptions.Timeout:
        return "Error: The request to the translation server timed out."
    except requests.exceptions.RequestException as e:
        return f"Error: An error occurred while trying to connect to the translation server: {e}"


# Define LibreTranslateLocally class
class LibreTranslateLocally:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Hello", "multiline": True}),
                "source": (names, ),
                "target": (names, ),
            }
        }

    # Align RETURN_TYPES properly
    RETURN_TYPES = ("STRING",)  
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "Translation"

    def execute(self, text, source, target):
        # Convert names to codes using the mapping
        source_code = name_to_code.get(source)
        target_code = name_to_code.get(target)
        if source_code and target_code:
            translated_text = translate_text_locally(text, source_code, target_code)
        else:
            return ("Error: Invalid language selection.", )
        
        # Return the main translation
        return (translated_text,)

# Define LibreTranslateOnline class , must fixed first
class LibreTranslateOnline:
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Hello", "multiline": True}),
                "source": (names, ),
                "target": (names, ),
                "api_key": ("STRING", {}),
            }
        }

    # Align RETURN_TYPES properly
    RETURN_TYPES = ("STRING",)  
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "Translation"

    def execute(self, text, source, target, api_key):
        # Convert names to codes using the mapping
        source_code = name_to_code.get(source)
        target_code = name_to_code.get(target)
        if source_code and target_code:
            translated_text = translate_text_online(text, source_code, target_code, api_key)
        else:
            return ("Error: Invalid language selection.", )
        
        # Return the main translation
        return (translated_text,)

# Define node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "LibreTranslateLocally": LibreTranslateLocally,
    #"LibreTranslateOnline": LibreTranslateOnline,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LibreTranslateLocally": "Libre Translate Locally",
    #"LibreTranslateOnline": "Libre Translate Online",
}
