"""" Responsible for user input and displaying the current GameState """

from engine import GameState
from settings import Settings
from typing import List
import pygame
import os

WIDTH = HEIGHT = 1000
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


class Game:
    def __init__(self):
        pass


class GUI:
    """ Responsible for drawing the GUI """

    def __init__(self, settings: Settings, board: List[list[str]]):
        self.settings = settings
        self.board = board
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))

    def draw(self):
        self._draw_board()
        self._draw_pieces()

    def load_images(self) -> None:
        pieces = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
        for piece in pieces:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(os.path.abspath(f'../images/{piece}.png')),
                                                   (SQUARE_SIZE, SQUARE_SIZE))

    def _draw_square(self, row: int, col: int) -> None:
        color = self.settings.colors[((row + col) % 2)]
        square = pygame.Rect(left=col * self.settings.SQUARE_SIZE, top=row * self.settings.SQUARE_SIZE,
                             width=self.settings.SQUARE_SIZE, height=self.settings.SQUARE_SIZE)
        pygame.draw.rect(surface=self.screen, color=color, rect=square)

    def _draw_board(self) -> None:
        for row in range(self.settings.DIMENSION):
            for col in range(self.settings.DIMENSION):
                self._draw_square(row=row, col=col)

    def _draw_piece(self, row: int, col: int) -> None:
        piece = self.board[row][col]
        # not empty
        if piece != "--":
            self.screen.blit(IMAGES[piece],
                             pygame.Rect(col * self.settings.SQUARE_SIZE, row * self.settings.SQUARE_SIZE,
                                         self.settings.SQUARE_SIZE, self.settings.SQUARE_SIZE))

    def _draw_pieces(self) -> None:
        for row in range(self.settings.DIMENSION):
            for col in range(self.settings.DIMENSION):
                self._draw_piece()


def load_images():
    pieces = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(os.path.abspath(f'../images/{piece}.png')),
                                               (SQUARE_SIZE, SQUARE_SIZE))


# Responsible for all graphics with current game state.
def draw_game_state(screen, gamestate):
    draw_board(screen)
   # draw_pieces(screen, gamestate.board)


def draw_board(screen):
    """ drawing column by row, col * squaresize"""
    colors = [pygame.Color('white'), pygame.Color('blue')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            # not empty
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


# Move to engine.py
# Store move log and current state of the board
# if you capture a piece, remove it from the current state
# If we undo we need to store the piece that was captured, and the piece that did the capturing.

class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}  # rows are called ranks in chess
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}  # cols are called files in chess
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]  # could be an empty square

    def get_chess_notation(self):
        # File then rank, e.g. A5, E4
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
  #  clock = pygame.time.Clock()
  #  screen.fill((pygame.Color("white")))
    gs = GameState()
  #  load_images()  # load images
    running = True
    square_selected = ()  # no square selected, keep track of last click of the user
    player_clicks = []  # keep track of player clicks (two tuples)

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()  # (x,y) location of mouse
                col = location[0] // SQUARE_SIZE  ## x coordinate divided by square size
                row = location[1] // SQUARE_SIZE  # y
                if square_selected == (row, col):  # user clicked same square twice (undo)
                    square_selected = ()  # unselect
                    player_clicks = []  # reset player clicks
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)  # append for both 1st and 2nd clicks
                # Was that the users second click
                if len(player_clicks) == 2:  # after 2nd click
                    # make move
                    move = Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.make_move(move)
                    # Reset player clicks
                    square_selected = ()
                    player_clicks = []

        draw_game_state(screen, gs)
       # clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
