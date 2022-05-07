import logging

import pygame
from .event_handler import EventHandler
from .gui import GUI
from .settings import Settings
from .state import GameState

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
        logger.debug("Game started")

        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()  # (x,y) location of mouse
                    col = location[0] // self.settings.SQUARE_SIZE
                    row = location[1] // self.settings.SQUARE_SIZE
                    # Left click
                    if e.button == 1:
                        # TODO: Add highlighting when the square is clicked.
                        self.event_handler.left_click_square(row, col)
                    # Right click
                    elif e.button == 3:
                        self.event_handler.right_click_square(row, col)
                elif e.type == pygame.KEYDOWN:
                    self.event_handler.press_key(key=e.key)

            self.gui.draw()
            pygame.display.flip()


def main():
    chess_game = Game()
    chess_game.start()


if __name__ == "__main__":
    main()
