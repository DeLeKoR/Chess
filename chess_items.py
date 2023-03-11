import pygame
from options import *
pygame.init()
fnt_num = pygame.font.Font(pygame.font.get_default_font(), 24)

class Chessboard():
    def __init__(self, parent_surfuse: pygame.Surface, cell_qty=CELL_QTY, cell_size=size_field):
        self.__screen = parent_surfuse
        self.__qty = cell_qty
        self.__size = cell_size
        self.__all_cells = pygame.sprite.Group()
        self.__draw_playboard()
        pygame.display.update()
    def __draw_playboard(self):
        total_width = self.__qty * self.__size
        num_fields = self.__create_num_fields()
        self.__all_cells = self.__create_all_cells()
        num_fields_depth = num_fields[0].get_width()
        playboard_veiw = pygame.Surface((
            2 * num_fields_depth + total_width,
            2 * num_fields_depth + total_width
        )).convert_alpha()

        playboard_veiw.blit(num_fields[0], (0, num_fields_depth))
        playboard_veiw.blit(num_fields[0], (num_fields_depth + total_width, num_fields_depth))
        playboard_veiw.blit(num_fields[1], (num_fields_depth, 0))
        playboard_veiw.blit(num_fields[1], (num_fields_depth, num_fields_depth + total_width))

        playboard_rect = playboard_veiw.get_rect()
        playboard_rect.x += (self.__screen.get_width() - playboard_rect.width)//2
        playboard_rect.y += (self.__screen.get_height() - playboard_rect.height)//2
        self.__screen.blit(playboard_veiw, playboard_rect)
        cell_offset = (playboard_rect.x + num_fields_depth,
                       playboard_rect.y + num_fields_depth,)

        self.__draw_cells_on_playbord(cell_offset)


    def __create_num_fields(self):
        n_lines = pygame.Surface((self.__qty * self.__size, self.__size // 3)).convert_alpha()
        n_rows = pygame.Surface((self.__size // 3, self.__qty * self.__size)).convert_alpha()
        for i in range(0, self.__qty):
            letter = fnt_num.render(LTRS[i], True, WHITE)
            number = fnt_num.render(str(self.__qty - i), True, WHITE)
            n_lines.blit(letter, (
                i * self.__size + (self.__size - letter.get_rect().width) // 2,
                (n_lines.get_height() - letter.get_rect().height) // 2
            ))
            n_rows.blit(number, (
                (n_rows.get_width() - letter.get_rect().width) // 2,
                i * self.__size + (self.__size - number.get_rect().height) // 2
            ))
        return (n_rows, n_lines)


    def __create_all_cells(self):
        group = pygame.sprite.Group()
        is_even_qty = (self.__qty % 2 == 0)
        cell_color_index = 1 if is_even_qty else 0
        for y in range(self.__qty):
            for x in range(self.__qty):
                cell = Cell(cell_color_index, self.__size, (x, y), LTRS[x] + str(self.__qty - y))
                group.add(cell)
                cell_color_index ^= True
            cell_color_index = cell_color_index ^ True if is_even_qty else cell_color_index
        return group

    def __draw_cells_on_playbord(self, offset):
        for cell in self.__all_cells:
            cell.rect.x += offset[0]
            cell.rect.y += offset[1]
        self.__all_cells.draw(self.__screen)
class Cell(pygame.sprite.Sprite):
    def __init__(self, color_index: int, size: int, coords: tuple, name: str):
        super().__init__()
        x, y = coords
        self.color = color_index
        self.image = pygame.image.load(IMG_PATH + COLORS[color_index])
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = pygame.Rect(x * size, y * size, size, size)
