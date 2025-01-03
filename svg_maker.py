import chess
import chess.svg
import chess.pgn

# is this pgn for Black or White (which side are you learning?)
playing_as = chess.BLACK

#opening name
opening = 'Spanish'

# opening pgn, setting up board
pgn = open("Spanish_vs_for Black_____.__.__.pgn")
game = chess.pgn.read_game(pgn)
board_orientation = playing_as

# creates a list containing two SVGs for the front and back of a card
def create_svg(board1, board2, move1, move2):
    svgs = []
    svgs.append(chess.svg.board(board1,lastmove=move1,orientation=board_orientation,coordinates=False, size = 500))
    svgs.append(chess.svg.board(board2,lastmove=move2,orientation=board_orientation,coordinates=False, size = 500))
    return svgs

# recursively seraches through game, creating svgs
def goThroughGame(notes, node):
    for v in node.variations:
        if node.turn() == playing_as and node.ply() > 6:
            notes.append(create_svg(node.board(), v.board(), node.move, v.move))
        notes = goThroughGame(notes, v)
    return notes

notes = goThroughGame([], game)
print(len(notes))

for i in range(len(notes)):
    with open(f"{opening}{i}f.svg", "w") as f:
        f.write(notes[i][0])
    with open(f"{opening}{i}b.svg", "w") as f:
        f.write(notes[i][1])