import requests
import json
from dotenv import load_dotenv
import os


load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

translate_url = "https://api-free.deepl.com/v2/document"
translate_status_url = "https://api-free.deepl.com/v2/document/{0}"
translate_download_url = "https://api-free.deepl.com/v2/document/{0}/result"

def translate(data, source_lang="EN", target_lang="RU"):

    _params = {
        "source_lang" : source_lang,
        "auth_key" : DEEPL_API_KEY,
        "target_lang" : target_lang
    }

    response = requests.post(
        translate_url,params = _params,
        files = {"file": data}
    )
    
    jdata = json.loads(response.text)
    print(jdata)
    return {"id": jdata["document_id"], "key": jdata["document_key"]}

def checkStatus(id, key):

    _params = {
        "auth_key" : DEEPL_API_KEY,
        "document_key" : key
    }
    
    response = requests.get(translate_status_url.format(id),params=_params)
    
    return response.text

def writeToFile(id, key):

    _params = {
        "auth_key" : DEEPL_API_KEY,
        "document_key" : key
    }

    response = requests.get(
        translate_download_url.format(id),
        params = _params,
        allow_redirects = True
    )

    return response.content