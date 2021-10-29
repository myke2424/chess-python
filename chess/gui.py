import logging
import os
import sys
from typing import List

import pygame
from constants import EMPTY_SQUARE
from settings import Settings

logger = logging.getLogger(__name__)


class GUI:
    """ Responsible for drawing the GUI (board, pieces, highlighting etc) """

    def __init__(self, settings: Settings, board: List[List[str]]):
        self.board = board
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.square_size = settings.SQUARE_SIZE
        self.board_colors = [pygame.Color(color) for color in settings.BOARD_COLORS]
        self.piece_images = {}

        self._load_piece_images(image_dir=settings.IMAGE_DIR)

    def draw(self) -> None:
        """ Main interface used to draw the entire gui """
        self._draw_board()
        self._draw_pieces()

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

    def _draw_piece(self, row: int, col: int) -> None:
        """ Draw the piece on the given square (row/col) """
        piece = self.board[row][col]
        # TODO: Refactor to an enum?
        if piece != EMPTY_SQUARE:
            square = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
            # 'blit' draws the image on the screen on the given square (piece.name has a 1-to-1 mapping to an img name)
            self.screen.blit(self.piece_images[piece.name], square)

    def _draw_pieces(self) -> None:
        """ Draw all the pieces on the chess board """
        for row in range(8):
            for col in range(8):
                self._draw_piece(row, col)

    @staticmethod
    def _load_and_scale_image(image_path: str, width: int, height: int) -> pygame.Surface:
        """ Load and re-scale the image to the specified width/height """
        return pygame.transform.scale(pygame.image.load(os.path.abspath(image_path)), (width, height))

    def _load_piece_images(self, image_dir: str) -> None:
        """ Load all the piece images into self.peace_images dict. """

        if not os.path.exists(image_dir):
            logger.error(f"Image path: '{image_dir}' doesnt exist. Failed to load images. Exiting")
            sys.exit(1)

        images = os.listdir(image_dir)

        for image_path in images:
            piece = image_path.split(".")[0]  # get the filename without ext
            loaded_piece_image = self._load_and_scale_image(
                image_path=f"{image_dir}/{image_path}", width=self.square_size, height=self.square_size
            )
            self.piece_images[piece] = loaded_piece_image
