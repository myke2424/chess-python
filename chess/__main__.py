import pygame

from state import GameState
from settings import Settings
from gui import GUI
from event_handler import EventHandler


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
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()  # (x,y) location of mouse
                    col = location[0] // self.settings.SQUARE_SIZE
                    row = location[1] // self.settings.SQUARE_SIZE

                    self.event_handler.click_square(row, col)

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
