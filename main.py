import pygame
import sys

def run():
    pygame.init()
    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("Шахматы")
    bg_color = (180, 60, 20)
    FPS = 10
    length_width = 8
    size_field = 100
    colors_field = ((240, 240, 240), (10, 10, 10))
    TRS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    screen.fill(bg_color)
    FNT = pygame.font.Font(pygame.font.get_default_font(), 24)
    clock = pygame.time.Clock()

    even = length_width % 2 == 0
    color_index = 1 if even else 0
    for y in range(length_width):# отрисовка поля
        for x in range(length_width):
            pygame.draw.rect(screen, colors_field[color_index], (x*size_field, y*size_field, size_field, size_field))
            color_index ^= True
        color_index = color_index ^ True if even else color_index

    for i in range(0, length_width):# отрисовка цифр и букв
        letter = FNT.render(TRS[i], True, (255, 255, 255))
        numders = FNT.render(str(length_width - i), True, (255, 255, 255))
        screen.blit(letter, (i * size_field + size_field // 2 - size_field * 0.05,
                    size_field * length_width + (size_field // 4))
                    )
        screen.blit(numders, (size_field * length_width + (size_field // 4),
                    i * size_field + size_field // 2 - size_field * 0.05)
                    )


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(FPS)
        pygame.display.flip()

run()
