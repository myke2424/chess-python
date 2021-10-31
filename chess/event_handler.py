import logging

from chess_notation import ChessNotationParser
from move import Move
from state import GameState
from utils import EMPTY_SQUARE, Square

logger = logging.getLogger(__name__)


class EventHandler:
    """ Responsible for handling player inputs (events) """

    def __init__(self, state: GameState):
        """
        state: State of the game
        player_clicks: Keeps track of player clicks on a square.
                       It can only contain a max of two clicks (starting square clicked, destination square clicked)
        squared_clicked: Tuple containing row/col of the square the player clicked.
        """
        self.state = state
        self.player_clicks = 0
        self.first_click_location = None
        self.second_click_location = None

        self.event_key_map = {
            "UNDO_MOVE": ord("u"),
            "REDO_MOVE": ord("r"),
            "TURN": ord("t"),
            "RESET_GAME": ord("z"),
            "SCORE": ord("s"),
            "VALID_MOVES": ord("v"),
        }

    def left_click_square(self, row: int, col: int) -> None:
        """
        Mouse click handler when a square on the board is clicked.
        :param row: Row of the square clicked.
        :param col: Column of the square clicked
        :return:
        """
        square_clicked = Square(row, col)
        logger.debug(f"Player Clicked: {square_clicked} '{ChessNotationParser.from_row_and_col(row, col)}'")

        if self.first_click_location is None:
            self.first_click_location = square_clicked
        else:
            self.second_click_location = square_clicked

        self.player_clicks += 1

        # Reset clicks if user is trying to move a piece on the same square
        if self.first_click_location == self.second_click_location:
            self._reset_clicks()

        # If the user has clicked two squares (starting square and destination square), make the move
        if self.player_clicks == 2:
            move = Move(
                start_square=self.first_click_location,
                dest_square=self.second_click_location,
                board=self.state.board,
            )

            self.state.make_move(move)
            self._reset_clicks()

    def right_click_square(self, row: int, col: int) -> None:
        """ Return the state of the square when right clicked (Shows the piece on it / if its empty) """
        clicked = self.state.board[row][col]

        chess_notation = ChessNotationParser.from_row_and_col(row, col)
        if clicked == EMPTY_SQUARE:
            logger.debug(f"{chess_notation} = EMPTY SQUARE")
        else:
            logger.debug(f"{chess_notation} = {clicked} {clicked.pos_chess_notation}")

    def press_key(self, key: int) -> None:
        """
        handler for when keys are pressed.
        :param key: Unicode representation of the key
        """
        # Press 'u' to undo your last move
        if key == self.event_key_map["UNDO_MOVE"]:
            self.state.undo_move()
        elif key == self.event_key_map["REDO_MOVE"]:
            self.state.redo_move()
        elif key == self.event_key_map["TURN"]:
            logger.debug(self.state.turn)
        elif key == self.event_key_map["RESET_GAME"]:
            self.state.reset_game()
        elif key == self.event_key_map["SCORE"]:
            logger.debug(self.state.score)
        elif key == self.event_key_map["VALID_MOVES"]:
            self.state.print_valid_moves()

    def _reset_clicks(self) -> None:
        """ After the player makes their move, reset the player clicks/square clicked """
        self.first_click_location = None
        self.second_click_location = None
        self.player_clicks = 0
