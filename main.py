import pygame
import sys
from options import *
from chess_bord import *

def run():
    pygame.init()
    screen = pygame.display.set_mode((window_size))
    pygame.display.set_caption("Шахматы")
    screen.fill(bg_color)
    clock = pygame.time.Clock()

    checbord = Chessboard(screen)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(FPS)
        pygame.display.flip()

if __name__ == '__main__':
    run()
