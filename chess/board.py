import pygame
import os
import sys

pygame.init()

board_img = os.path.abspath('../images/chess-board.jpg')
board = pygame.image.load(board_img)
board = pygame.transform.scale(board, (1000, 1000))
height = 1000
width = 1000

white = (255, 64, 64)

screen = pygame.display.set_mode(size=(width, height))
# screen.fill(white)
pygame.display.set_caption("CHESS")

run = True

# GameState data structure that represents board
# Possible moves
# Guess whos winning based on weight of pieces
# calculate legal moves

while run:
    screen.blit(board, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pass
