import pygame
from options import *
pygame.init()
fnt_num = pygame.font.Font(pygame.font.get_default_font(), 24)

class Chessboard():
    def __init__(self, parent_surfuse: pygame.Surface, cell_qty=CELL_QTY, cell_size=size_field):
        self.__screen = parent_surfuse
        self.__draw_playboard(cell_qty, cell_size)
        pygame.display.update()
    def __draw_playboard(self, cell_qty, cell_size):
        total_width = cell_qty * cell_size
        num_fields = self.__create_num_fields(cell_qty, cell_size)
        fields = self.__create_all_cells(cell_qty, cell_size)
        num_fields_depth = num_fields[0].get_width()
        playboard_veiw = pygame.Surface((
            2 * num_fields_depth + total_width,
            2 * num_fields_depth + total_width
        )).convert_alpha()

        playboard_veiw.blit(num_fields[0], (0, num_fields_depth))
        playboard_veiw.blit(num_fields[0], (num_fields_depth + total_width, num_fields_depth))
        playboard_veiw.blit(num_fields[1], (num_fields_depth, 0))
        playboard_veiw.blit(num_fields[1], (num_fields_depth, num_fields_depth + total_width))
        playboard_veiw.blit(fields, (num_fields_depth, num_fields_depth))

        playboard_rect = playboard_veiw.get_rect()
        playboard_rect.x += (self.__screen.get_width() - playboard_rect.width)//2
        playboard_rect.y += (self.__screen.get_height() - playboard_rect.height)//2
        self.__screen.blit(playboard_veiw, playboard_rect)

    def __create_num_fields(self, cell_qty, cell_size):
        n_lines = pygame.Surface((cell_qty * cell_size, cell_size // 3)).convert_alpha()
        n_rows = pygame.Surface((cell_size // 3, cell_qty * cell_size)).convert_alpha()
        for i in range(0, cell_qty):
            letter = fnt_num.render(LTRS[i], True, WHITE)
            number = fnt_num.render(str(cell_qty - i), True, WHITE)
            n_lines.blit(letter, (
                i * cell_size + (cell_size - letter.get_rect().width) // 2,
                (n_lines.get_height() - letter.get_rect().height) // 2
            ))
            n_rows.blit(number, (
                (n_rows.get_width() - letter.get_rect().width) // 2,
                i * cell_size + (cell_size - number.get_rect().height) // 2
            ))
        return (n_rows, n_lines)


    def __create_all_cells(self, cell_qty, cell_size):
        fields = pygame.Surface((cell_qty * cell_size, cell_size * cell_qty)).convert_alpha()
        is_even_qty = (cell_qty % 2 == 0)
        cell_color_index = 1 if is_even_qty else 0
        for y in range(cell_qty):
            for x in range(cell_qty):
                cell = pygame.Surface((cell_size, cell_size))
                cell.fill(COLORS[cell_color_index])
                fields.blit(cell, (x * cell_size, y * cell_size))
                cell_color_index ^= True
            cell_color_index = cell_color_index ^ True if is_even_qty else cell_color_index
        return fields

