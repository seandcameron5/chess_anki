import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

invoke('createDeck', deck='Spanish')
params = {
        "note": {
            "deckName": "Spanish",
            "modelName": "Basic",
            "fields": {
                "Front": "",
                "Back": ""
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": "Spanish",
                    "checkChildren": False,
                    "checkAllModels": False
                }
            },
            "picture": [{
                "path": r"C:\Users\seans\chess_anki\italian4b.svg",
                "filename": "italian4b.svg",
                "fields": [
                    "Back"
                ]
            },
            {
                "path": r"C:\Users\seans\chess_anki\italian4w.svg",
                "filename": "italian4w.svg",
                "fields": [
                    "Front"
                ]
            }]

        }
    }

invoke('addNote', **params)