import os
import json
import urllib.request

CURRENT_DIRECTORY = os.getcwd()


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

def generate_params(deckName: str, fields: list[str], file_names: list[str], field_texts: list[str] = None):
    return {
        "note": {
            "deckName": deckName,
            "modelName": "Basic",
            "fields": {
                field: text for field, text in zip(fields, field_texts if field_texts else ["" for _ in fields])
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
                "duplicateScopeOptions": {
                    "deckName": deckName,
                    "checkChildren": False,
                    "checkAllModels": False
                }
            },
            "picture": [
                {
                    "path": CURRENT_DIRECTORY+r"\\"+file_name,
                    "filename": file_name,
                    "skipHash": "8d6e4646dfae812bf39651b59d7429ce",
                    "fields": [
                        field
                    ]
                } for field, file_name in zip(fields, file_names)
            ]
        }
    }

opening = "Spanish"
invoke('createDeck', deck=opening)


params = []
for i in range(69):
    params.append(generate_params(deckName=opening, fields=["Front", "Back"], file_names=[opening+f'{i}'+'f.svg', opening+f'{i}'+'b.svg']))

for p in params:
    invoke('addNote', **p)