import os

CURRENT_DIRECTORY = os.getcwd()

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
                    "deckName": "Spanish",
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


print(generate_params(deckName="TestDeck", fields=["Front", "Back"], file_names=["normal_file1", "normal_file2"]))