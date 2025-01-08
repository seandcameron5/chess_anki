import chess
import chess.svg
import chess.pgn
import os
import json
import urllib.request
from stockfish import Stockfish


# is this pgn for Black or White (which side are you learning?)
playing_as = chess.WHITE

#opening name
opening = 'Evan\'s Gambit (W)'

# opening pgn, setting up board
pgn = open("evansGambit_forwhite.pgn")
game = chess.pgn.read_game(pgn)
board_orientation = playing_as
engine = chess.engine.SimpleEngine.popen_uci("stockfish-windows-x86-64-avx2.exe")


# Definition of functions used to generate cards and place cards into Anki deck
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
            "modelName": "Chess Openings v2",
            "fields": {
                field: text for field, text in zip(fields, field_texts if field_texts else ["" for _ in fields])
            },
            "options": {
                "allowDuplicate": True,
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
                } for field, file_name in zip(fields[0:2], file_names)
            ]
        }
    }
# creates a list containing two SVGs for the front and back of a card
def create_svg(board1, board2, move1, move2, comment1, comment2):
    svgs = []
    svgs.append(chess.svg.board(board1,lastmove=move1,orientation=board_orientation,coordinates=False, size = 500))
    svgs.append(chess.svg.board(board2,lastmove=move2,orientation=board_orientation,coordinates=False, size = 500))
    eval = engine.analyse(board1, chess.engine.Limit(time=1))["score"].white().score() / 100
    #eval2 = engine.analyse(board2, chess.engine.Limit(time=0.2))["score"].white().score() / 100
    print(eval)
    svgs.append(comment1)
    svgs.append(comment2 )
    svgs.append(str(eval))
    return svgs

# recursively seraches through game, creating svgs
def goThroughGame(notes, node):
    for v in node.variations:
        if node.turn() == playing_as and node.ply() >= 0:
            notes.append(create_svg(node.board(), v.board(), node.move, v.move, node.comment, v.comment))
        notes = goThroughGame(notes, v)
    return notes


# generating images for notes
notes = goThroughGame([], game)
for i in range(len(notes)):
    with open(f"{opening}{i}f.svg", "w") as f:
        f.write(notes[i][0])
    with open(f"{opening}{i}b.svg", "w") as f:
        f.write(notes[i][1])


# Creating deck to store notes
CURRENT_DIRECTORY = os.getcwd()
invoke('createDeck', deck=opening)

# adding notes
params = []
for i in range(len(notes)):
    params.append(generate_params(deckName=opening, fields=["Move", "Response", "Comment (Front)", "Comment (Back)", "Evaluation (Back)"], file_names=[opening+f'{i}'+'f.svg', opening+f'{i}'+'b.svg'], field_texts=["", "", notes[i][2], notes[i][3], notes[i][4]]))

for p in params:
    invoke('addNote', **p)

for i in range(len(notes)):
    os.remove(f"{opening}{i}f.svg")
    os.remove(f"{opening}{i}b.svg")