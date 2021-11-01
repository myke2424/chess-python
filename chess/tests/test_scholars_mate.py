import pytest

from ..state import GameState
from ..move import Move


def test_scholars_mate() -> None:
    game_state = GameState()
    scholar_mate_move_sequence = ("e2->e4", "e8->e6", "f1->c4", "a7->a6", "d1->h5", "e6->e5", "h5->f7")
    moves = [Move.from_chess_notation(notation=move, board=game_state.board) for move in scholar_mate_move_sequence]

    for move in moves:
        game_state.make_move(move)

    assert game_state.checkmate is True
