import chess
import chess.svg
import chess.pgn
import os
import json
import urllib.request
from stockfish import Stockfish


pgn = open("ponzianiVulkovicGambit_forblack.pgn")
game = chess.pgn.read_game(pgn)
engine = chess.engine.SimpleEngine.popen_uci("stockfish-windows-x86-64-avx2.exe")
board = game.board()
for move in game.mainline_moves():
    board.push(move)
    print(engine.analyse(board, chess.engine.Limit(time=0.1))["score"].white().score() / 100)

