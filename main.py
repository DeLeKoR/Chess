import pygame
import sys

def run():
    pygame.init()
    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("Шахматы")
    bg_color = (180, 60, 20)
    clock = pygame.time.Clock()
    FPS = 10
    screen.fill(bg_color)
    length_width = 8
    size_field = 100
    colors_field = ((200, 200, 200), (10, 10, 10))

    even = length_width % 2 == 0
    color_index = 1 if even else 0
    for y in range(length_width):
        for x in range(length_width):
            pygame.draw.rect(screen, colors_field[color_index], (x*size_field, y*size_field, size_field, size_field))
            color_index ^= True
        color_index = color_index ^ True if even else color_index


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(FPS)
        pygame.display.flip()

run()
