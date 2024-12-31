import chess
import chess.svg
import chess.pgn


# is this pgn for Black or White (which side are you learning?)
playing_as = chess.BLACK

#opening name
opening = 'italian'

# opening pgn, setting up board
pgn = open("__vs_______.__.__.pgn")
game = chess.pgn.read_game(pgn)
board = game.board()

#list of svgs
svgs = []
svgs_variations = []
board_orientation = playing_as

#generates svg's for mainline
mainline_moves_count = 0
for move in game.mainline_moves():
    board.push(move)
    svgs.append(chess.svg.board(board,lastmove=move,orientation=board_orientation,coordinates=False, size = 350))
    mainline_moves_count += 1


# creates a list containing two SVGs for the front and back of a card
def create_svg(board1, board2):
    svgs = []
    svgs.append(chess.svg.board(board1,lastmove=move,orientation=board_orientation,coordinates=False, size = 350))
    svgs.append(chess.svg.board(board2,lastmove=move,orientation=board_orientation,coordinates=False, size = 350))
    return svgs

# recursively seraches through game, creating svgs
def goThroughGame(notes, node):
    print(node.board())
    for v in node.variations:
        if node.turn() == playing_as and node.ply() > 1:
            notes.append(create_svg(node.board(), v.board()))
        return goThroughGame(notes, v)
    print('returning notes')
    return notes

notes = goThroughGame([], game)
print(len(notes))

for i in range(len(notes)):
    with open(f"{opening}{i}w.svg", "w") as f:
        f.write(notes[i][0])
    with open(f"{opening}{i}b.svg", "w") as f:
        f.write(notes[i][1])




for i in range(0, 6):
    if i % 2 == 0:
        with open(f"{opening}{i // 2 + 1}w.svg", "w") as f:
            f.write(svgs[i])
    else:
        with open(f"{opening}{i // 2 + 1}b.svg", "w") as f:
            f.write(svgs[i])