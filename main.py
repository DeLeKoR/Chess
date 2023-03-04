import pygame
import sys

def run():
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption("Шахматы")
    bg_color = (90, 120, 20)
    clock = pygame.time.Clock()
    FPS = 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(FPS)
        screen.fill(bg_color)
        pygame.display.flip()


run()