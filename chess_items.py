from pieces import *
import board_data
pygame.init()
fnt_num = pygame.font.Font(pygame.font.get_default_font(), 24)

class Chessboard:
    def __init__(self, parent_surfuse: pygame.Surface, cell_qty=CELL_QTY, cell_size=size_field):
        self.__screen = parent_surfuse
        self.__table = board_data.board
        self.__qty = cell_qty
        self.__size = cell_size
        self.__pieces_types = PIECES_TYPES
        self.__all_cells = pygame.sprite.Group()
        self.__all_pieces = pygame.sprite.Group()
        self.__draw_playboard()
        self.__draw_all_pieces()
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

    def __draw_all_pieces(self):
        self.__setup_board()
        self.__all_pieces.draw(self.__screen)

    def __setup_board(self):
        for j, row in enumerate(self.__table):
            for i, field_value in enumerate(row):
                if field_value != 0:
                    piece = self.__create_piece(field_value, (j, i))
                self.__all_pieces.add(piece)
        for piece in self.__all_pieces:
            for cell in self.__all_cells:
                if piece.field_name == cell.field_name:
                    piece.rect = cell.rect

    def __create_piece(self, piece_symbol: str, table_coord: tuple):
        field_name = self.__to_field_name(table_coord)
        piece_tuple = self.__pieces_types[piece_symbol]
        classname = globals()[piece_tuple[0]]
        return classname(self.__size, piece_tuple[1], field_name)

    def __to_field_name(self, table_coord: tuple):
        return LTRS[table_coord[1]] + str(self.__qty - table_coord[0])
class Cell(pygame.sprite.Sprite):
    def __init__(self, color_index: int, size: int, coords: tuple, name: str):
        super().__init__()
        x, y = coords
        self.color = color_index
        self.field_name = name
        self.image = pygame.image.load(IMG_PATH + COLORS[color_index])
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = pygame.Rect(x * size, y * size, size, size)
