import chess
import chess.svg
import chess.pgn


# is this pgn for Black or White (which side are you learning?)
playing_as = chess.BLACK

#opening name
opening = 'spanish'

# opening pgn, setting up board
pgn = open("Spanish_vs_for Black_____.__.__.pgn")
game = chess.pgn.read_game(pgn)
board = game.board()

#list of svgs
svgs = []
board_orientation = playing_as

#generates svg's for mainline
mainline_moves_count = 0
for move in game.mainline_moves():
    mainline_moves_count += 1
    board.push(move)
    svgs.append(chess.svg.board(board,lastmove=move,orientation=board_orientation,coordinates=False, size = 350))

print(game.variations)
#svgs_variations = []
#for variation in game.variations:
#    board.push(move)
#    svgs_variations.append(chess.svg.board(board,lastmove=move,orientation=board_orientation,coordinates=False, size = 350))

for i in range(0, 6):
    if i % 2 == 0:
        with open(f"{opening}{i // 2 + 1}w.svg", "w") as f:
            f.write(svgs[i])
    else:
        with open(f"{opening}{i // 2 + 1}b.svg", "w") as f:
            f.write(svgs[i])