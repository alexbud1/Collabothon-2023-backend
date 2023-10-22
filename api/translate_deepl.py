import os
from os.path import dirname, join 
from dotenv import load_dotenv
import deepl

# dotenv_path = join(dirname(__file__), ".env")
# load_dotenv(dotenv_path)
# DEEPL_API = os.environ.get("DEEPL_API")
# print(DEEPL_API)
DEEPL_API = '41cfe16a-4dc5-72f0-7d55-a4d656f9d865:fx'
translator = deepl.Translator(DEEPL_API)

#translate a string into english 
def translate_to_en(inp:str):
    result = translator.translate_text(inp, target_lang="EN-US")
    return result

#translate a string into polish
def translate_to_pl(inp:str):
    result = translator.translate_text(inp, target_lang="PL")
    return result
