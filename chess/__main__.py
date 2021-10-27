import pygame

from state import GameState
from settings import Settings
from gui import GUI
from move import Move


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
        self.player_clicks = []
        self.square_clicked = ()

    def click_square(self, row: int, col: int) -> None:
        self.square_clicked = (row, col)
        self.player_clicks.append(self.square_clicked)

        # If the user has clicked two squares (starting square and destination square), make the move
        if len(self.player_clicks) == 2:
            move = Move(starting_square=self.player_clicks[0], destination_square=self.player_clicks[1],
                        board=self.state.board)

            self.state.make_move(move)
            self._reset_clicks()

    def _reset_clicks(self) -> None:
        """ After the player makes their move, reset the player clicks/square clicked """
        self.player_clicks.clear()
        self.square_clicked = ()


class Game:
    """ Main class that represents the entire game """

    def __init__(self):
        self.state = GameState()
        self.settings = Settings
        self.gui = GUI(settings=self.settings, board=self.state.board)
        self.event_handler = EventHandler(state=self.state)
        self.running = True

    def start(self) -> None:
        """ Main interface used to start the game of chess """
        pygame.init()

        while self.running:
            # TODO: Refactor user input into a EventQueue class?
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()  # (x,y) location of mouse
                    col = location[0] // self.settings.SQUARE_SIZE
                    row = location[1] // self.settings.SQUARE_SIZE

                    self.event_handler.click_square(row, col)

                    print(f"row: {row}, col: {col}")
                    # Mouse button down = player click
                    # A Player needs to make two clicks
                    # Click the piece it wants to move, then click the destination piece
                    # So we can make 2 clicks, once the player has made two clicks, make the move then reset the clicks

                #     if square_selected == (row, col):  # user clicked same square twice (undo)
                #         square_selected = ()  # unselect
                #         player_clicks = []  # reset player clicks
                #     else:
                #         square_selected = (row, col)
                #         player_clicks.append(square_selected)  # append for both 1st and 2nd clicks
                #     # Was that the users second click
                #     if len(player_clicks) == 2:  # after 2nd click
                #         # make move
                #         move = Move(player_clicks[0], player_clicks[1], gs.board)
                #         print(move.get_chess_notation())
                #         gs.make_move(move)
                #         # Reset player clicks
                #         square_selected = ()
                #         player_clicks = []
                #
                #     # If
                # else:
                #     pass

            self.gui.draw()
            pygame.display.flip()


def main():
    chess_game = Game()
    chess_game.start()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f'Error: {err}')
        raise err
