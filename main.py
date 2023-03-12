import sys

import pygame

from chess_items import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE))
pygame.display.set_caption("Шахматы")
screen.fill(BACKGROUND)
clock = pygame.time.Clock()

chessboard = Chessboard(screen, 8, 60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            chessboard.btn_down(event.button, event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            chessboard.btn_up(event.button, event.pos)
        if event.type == pygame.MOUSEMOTION:
            chessboard.drag(event.pos)
    clock.tick(FPS)
    pygame.display.flip()
