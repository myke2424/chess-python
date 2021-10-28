from piece import Bishop, King, Knight, Pawn, Queen, Rook

BLACKS_STARTING_KINGS_ROW = [
    Rook(color="b", row=0, col=0),
    Knight(color="b", row=0, col=1),
    Bishop(color="b", row=0, col=2),
    Queen(color="b", row=0, col=3),
    King(color="b", row=0, col=4),
    Bishop(color="b", row=0, col=5),
    Knight(color="b", row=0, col=6),
    Rook(color="b", row=0, col=7),
]

BLACKS_STARTING_PAWN_ROW = [
    Pawn(color="b", row=1, col=0),
    Pawn(color="b", row=1, col=1),
    Pawn(color="b", row=1, col=2),
    Pawn(color="b", row=1, col=3),
    Pawn(color="b", row=1, col=4),
    Pawn(color="b", row=1, col=5),
    Pawn(color="b", row=1, col=6),
    Pawn(color="b", row=1, col=7),
]

WHITES_STARTING_KINGS_ROW = [
    Rook(color="w", row=7, col=0),
    Knight(color="w", row=7, col=1),
    Bishop(color="w", row=7, col=2),
    Queen(color="w", row=7, col=3),
    King(color="w", row=7, col=4),
    Bishop(color="w", row=7, col=5),
    Knight(color="w", row=7, col=6),
    Rook(color="w", row=7, col=7),
]

WHITES_STARTING_PAWN_ROW = [
    Pawn(color="w", row=6, col=0),
    Pawn(color="w", row=6, col=1),
    Pawn(color="w", row=6, col=2),
    Pawn(color="w", row=6, col=3),
    Pawn(color="w", row=6, col=4),
    Pawn(color="w", row=6, col=5),
    Pawn(color="w", row=6, col=6),
    Pawn(color="w", row=6, col=7),
]
