import chess
import chess.svg
import chess.pgn


# is this pgn for Black or White (which side are you learning?)
forWhite = False

# opening pgn, setting up board
pgn = open("Spanish_vs_for Black_____.__.__.pgn")
game = chess.pgn.read_game(pgn)
board = game.board()

#list of svgs
svgs = []
mainline_moves_count = 0
for move in game.mainline_moves():
    mainline_moves_count += 1
    board.push(move)
    svgs.append(chess.svg.board(board, size = 350))

for i in range(5, mainline_moves_count + 1):
    with open(f"spanish_test{i}.svg", "w") as f:
        f.write(svgs[i])