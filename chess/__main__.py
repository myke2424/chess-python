import pygame
from engine import GameState
from settings import Settings
from gui import GUI


# class EventQueue:
#     @classmethod
#     def handler(cls):
#         for e in pygame.event.get():
#             if e.type == pygame.QUIT:
#                 game_running = False
#             else:
#                 pass


class Game:
    """ Main class that represents the entire game """

    def __init__(self):
        self.state = GameState()
        self.settings = Settings
        self.gui = GUI(settings=self.settings, board=self.state.board)
        self.running = True

    def start(self) -> None:
        """ Main interface used to start the game of chess """
        pygame.init()
        #EventQueue.handler()

        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sefl.running = False
                else:
                    pass

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
