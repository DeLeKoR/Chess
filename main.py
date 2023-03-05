import pygame
import sys

def run():
    pygame.init()
    window_size = (1200, 900)
    screen = pygame.display.set_mode((window_size))
    pygame.display.set_caption("Шахматы")
    bg_color = (180, 60, 20)
    FPS = 10
    size = 8
    size_field = 95
    colors_field = ((240, 240, 240), (20, 20, 20))
    TRS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    screen.fill(bg_color)
    FNT = pygame.font.Font(pygame.font.get_default_font(), 24)
    clock = pygame.time.Clock()

    n_lines =pygame.Surface((size*size_field, size_field // 2))
    n_rows = pygame.Surface((size_field // 2, size*size_field))
    fields = pygame.Surface((size*size_field, size*size_field))
    board = pygame.Surface((2*n_rows.get_width() + fields.get_width(), 2*n_lines.get_height() + fields.get_height()))

    even = size % 2 == 0
    color_index = 1 if even else 0
    for y in range(size):# отрисовка поля
        for x in range(size):
            #pygame.draw.rect(screen, colors_field[color_index], (x*size_field, y*size_field, size_field, size_field))
            cell = pygame.Surface((size_field, size_field)).convert_alpha()
            cell.fill(colors_field[color_index])
            fields.blit(cell, (x*size_field, y*size_field))
            color_index ^= True
        color_index = color_index ^ True if even else color_index

    for i in range(0, size):# отрисовка цифр и букв
        letter = FNT.render(TRS[i], True, (255, 255, 255))
        numders = FNT.render(str(size - i), True, (255, 255, 255))
        n_lines.blit(letter, (i*size_field + (size_field - letter.get_rect().width) // 2,
                     (n_lines.get_height() - letter.get_rect().height) // 2)
                    )
        n_rows.blit(numders, ((n_rows.get_width() - letter.get_rect().width)//2,
                     i * size_field + (size_field - numders.get_rect().height) // 2)
                    )

    board.blit(n_rows, (0, n_lines.get_height()))
    board.blit(n_rows, (n_rows.get_width() + fields.get_width(), n_lines.get_height()))
    board.blit(n_lines, (n_rows.get_width(), 0))
    board.blit(n_lines, (n_rows.get_width(), n_rows.get_width() + fields.get_width()))
    board.blit(fields, (n_rows.get_width(), n_lines.get_height()))
    screen.blit(board, ((window_size[0] - board.get_width()) // 2,
                        (window_size[1] - board.get_height()) // 2))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        clock.tick(FPS)
        pygame.display.flip()

run()
