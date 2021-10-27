import pygame
import os

from settings import Settings
from typing import List


class GUI:
    """ Responsible for drawing the GUI (board, pieces, highlighting etc)"""

    def __init__(self, settings: Settings, board: List[List[int]]):
        self.board = board
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.square_size = settings.SQUARE_SIZE
        self.board_colors = [pygame.Color(color) for color in settings.BOARD_COLORS]

    def draw(self) -> None:
        """ Main interface used to draw the entire gui """
        self._draw_board()
        # self.draw_pieces()

    def _draw_square(self, row: int, col: int) -> None:
        """ Draw one square on the board for the given row/col """
        color = self.board_colors[((row + col) % 2)]
        square = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
        pygame.draw.rect(surface=self.screen, color=color, rect=square)

    def _draw_board(self) -> None:
        """ Draw the 8x8 chess board """
        for row in range(8):
            for col in range(8):
                self._draw_square(row, col)
