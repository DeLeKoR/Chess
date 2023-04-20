import pygame.image
from pieces import *
from board_data import *
pygame.init()
fnt_num = pygame.font.Font(pygame.font.get_default_font(), 24)

class Chessboard:
    def __init__(self, cell_qty=CELL_QTY, cell_size=size_field):
        pygame.display.set_caption("Шахматы")
        self.__screen = pygame.display.set_mode((WINDOW_SIZE))
        self.table = board
        self.__qty = cell_qty
        self.__size = cell_size
        self.__pieces_types = PIECES_TYPES
        self.all_cells = pygame.sprite.Group()
        self.all_pieces = pygame.sprite.Group()
        self.all_areas = pygame.sprite.Group()
        self.all_free_cells = pygame.sprite.Group()
        self.all_attack_cells = pygame.sprite.Group()
        self.possible_moves = pygame.sprite.Group()
        self.pressed_cell = None
        self.picked_piece = None
        self.picked_cell = None
        self.dragged_piece = None
        self.down_position = None
        self.old_piece = None
        self.designated_cell = None
        self.draw_playboard()
        self.setup_board()
        self.grand_update()
        self.queue = 'w'
    def draw_playboard(self):
        self.__screen.fill(BACKGROUND)
        total_width = self.__qty * self.__size
        num_fields = self.create_num_fields()
        self.all_cells = self.create_all_cells()
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
        self.aplly_offset_for_cells(cell_offset)
    def create_num_fields(self):
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
    def create_all_cells(self):
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
    def aplly_offset_for_cells(self, offset):
        for cell in self.all_cells:
            cell.rect.x += offset[0]
            cell.rect.y += offset[1]
    def setup_board(self):
        for j, row in enumerate(self.table):
            for i, field_value in enumerate(row):
                if field_value != 0:
                    piece = self.create_piece(field_value, (j, i))
                self.all_pieces.add(piece)
        for piece in self.all_pieces:
            for cell in self.all_cells:
                if piece.field_name == cell.field_name:
                    piece.rect = cell.rect.copy()
    def create_piece(self, piece_symbol: str, table_coord: tuple = None, cord: bool = None):
        field_name = self.to_field_name(table_coord)
        if cord is not None:
            field_name = cord
        piece_tuple = self.__pieces_types[piece_symbol]
        classname = globals()[piece_tuple[0]]
        return classname(self.__size, piece_tuple[1], field_name)
    def to_field_name(self, table_coord: tuple):
        if table_coord is not None:
            return LTRS[table_coord[1]] + str(self.__qty - table_coord[0])

    def get_piece(self, position: tuple):
        for piece in self.all_pieces:
            if piece.rect.collidepoint(position):
                return piece
        return None

    def get_cell(self, position: tuple):
        for cell in self.all_cells:
            if cell.rect.collidepoint(position):
                return cell
        return None

    def get_cell_by_name(self, name):
        for cell in self.all_cells:
            if cell.field_name == name:
                return cell
        return None

    def get_free_cell(self, position: tuple):
        for cell in self.all_free_cells:
            if self.get_cell(position) == cell:
                return cell
        return None

    def get_piece_on_cell(self, cell):
        for piece in self.all_pieces:
            if piece.field_name == cell.field_name:
                return piece
        return None

    def get_straight_line_field(self, cell, mode: int):
        n = i = 1
        if mode == 1: # вверх
            i = 1
        elif mode == 2: # вниз
            i = -1
        elif mode == 3: # влево
            i, n = 1, 0
        elif mode == 4: # вправо
            i, n = -1, 0
        next_cell = list(cell.field_name)
        k = str(int(next_cell[1]) + i) if n == 1 else LTRS[LTRS.index(next_cell[0])+i]
        next_cell[n] = k
        next_cell = "".join(next_cell)
        for c in self.all_cells:
            if c.field_name == next_cell:
                return c

    def get_diagonal_field(self, cell, mode: int):
        j = i = 1
        if mode == 1:
            j = i = 1
        elif mode == 2:
            j, i = 1, -1
        elif mode == 3:
            j, i = -1, 1
        elif mode == 4:
            j = i = -1
        next_cell = list(cell.field_name)
        k = [LTRS[LTRS.index(next_cell[0]) + j], str(int(next_cell[1]) + i)]
        next_cell = k
        next_cell = "".join(next_cell)
        for c in self.all_cells:
            if c.field_name == next_cell:
                return c

    def get_g_field(self, cell, mode: int):
        i, j = 2, 1
        if mode == 1:
            i, j = 2, 1
        elif mode == 2:
            i, j = 1, 2
        elif mode == 3:
            i, j = 2, -1
        elif mode == 4:
            i, j = 1, -2
        elif mode == 5:
            i, j = -2, -1
        elif mode == 6:
            i, j = -1, -2
        elif mode == 7:
            i, j = -2, 1
        elif mode == 8:
            i, j = -1, 2
        next_cell = list(cell.field_name)
        k = [LTRS[LTRS.index(next_cell[0]) + j], str(int(next_cell[1]) + i)]
        next_cell = k
        next_cell = "".join(next_cell)
        for c in self.all_cells:
            if c.field_name == next_cell:
                return c

    def get_all_free_cells_for_piece(self, peace, cell=None):
        cell = cell if cell is not None else self.pressed_cell
        if peace.name == 'pawn' and peace.move:
            self.find_free_cells(cell, f'{peace.name}1')
            self.mark_free_fields()
        else:
            self.find_free_cells(cell, peace.name)
            self.mark_free_fields()

    def get_cell_king(self, color):
        for cell in self.all_cells:
            if self.check_pieces_on_cell(cell):
                if self.get_piece_on_cell(cell).name == 'king':
                    if self.get_piece_on_cell(cell).color == color:
                        return cell

    def get_king(self, color):
        for cell in self.all_cells:
            if self.check_pieces_on_cell(cell):
                if self.get_piece_on_cell(cell).name == 'king':
                    if self.get_piece_on_cell(cell).color == color:
                        return self.get_piece_on_cell(cell)

    def get_rook(self, mode):
        new_cell = self.get_cell_king(self.queue)
        if mode == 'left':
            while self.get_straight_line_field(new_cell, 3) is not None:
                new_cell = self.get_straight_line_field(new_cell, 3)
                if self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).name == 'rook':
                    return self.get_piece_on_cell(new_cell)
        else:
            while self.get_straight_line_field(new_cell, 4) is not None:
                new_cell = self.get_straight_line_field(new_cell, 4)
                if self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).name == 'rook':
                    return self.get_piece_on_cell(new_cell)

    def get_all_moves(self):
        self.possible_moves.empty()
        for peace in self.all_pieces:
            if self.queue == peace.color:
                cell = self.get_cell_by_name(peace.field_name)
                if peace.name == 'pawn':
                    self.find_free_cells(cell, f'{peace.name}1', 1)
                else:
                    self.find_free_cells(cell, peace.name, 1)
        self.grand_update()


    def straight_move(self, cell, free_cells):
        for i in range(1, 5):
            new_cell = cell
            while self.get_straight_line_field(new_cell, i) is not None:
                new_cell = self.get_straight_line_field(new_cell, i)
                if self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).color == self.queue:
                    break
                if self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).color != self.queue:
                    self.all_attack_cells.add(new_cell)
                    free_cells.add(new_cell)
                    break
                free_cells.add(new_cell)

    def diagonal_move(self, cell, free_cells):
        for i in range(1, 5):
            new_cell = cell
            while self.get_diagonal_field(new_cell, i) is not None:
                new_cell = self.get_diagonal_field(new_cell, i)
                if self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).color == self.queue:
                    break
                free_cells.add(new_cell)
                if self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).color != self.queue:
                    break

    def Check_castling(self, side):
        i = 3 if side else 4
        king = self.get_cell_king(self.queue)
        new_cell = king
        if self.get_piece_on_cell(king).move:
            while self.get_straight_line_field(new_cell, i) is not None:
                new_cell = self.get_straight_line_field(new_cell, i)
                if self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).name == 'rook':
                    if self.get_piece_on_cell(new_cell).move:
                        return True
                elif self.check_pieces_on_cell(new_cell):
                    break
            return False
        else:
            return False

    def check_shah(self):
        self.Queue()
        self.get_all_moves()
        self.Queue()
        cell_king = self.get_cell_king(self.queue)
        if self.check_cell_in_grope_cell(cell_king, self.possible_moves):
            return True
        else:
            return False

    def check_pieces_on_cell(self, cell):
        piece = self.get_piece_on_cell(cell)
        if piece is not None:
            return True
        else:
            return False

    def check_cell_in_grope_cell(self, cell, grope):
        for c in grope:
            if c.field_name == cell.field_name:
                return True
        return False

    def mark_free_fields(self):
        for cell in self.all_free_cells:
            if not cell in self.all_attack_cells:
                self.mark_cell(cell, 3)
        for cell in self.all_attack_cells:
            self.mark_cell(cell, 4)

    def pawn_killed(self, cell, free_cells):
        for i in range(1, 4, 2):
            i = i + 1 if self.queue == 'b' else i
            new_cell = cell
            if self.get_diagonal_field(new_cell, i) is not None:
                new_cell = self.get_diagonal_field(new_cell, i)
                if self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).color != self.queue:
                    free_cells.add(new_cell)
                else:
                    pass

    def pawn_move(self, cell, free_cells):
        i = 1 if self.queue == 'w' else 2
        if self.get_straight_line_field(cell, i) is not None:
            new_cell = self.get_straight_line_field(cell, i)
            if not self.check_pieces_on_cell(new_cell):
                free_cells.add(new_cell)
                return new_cell
            return cell

    def castling(self, cell, peace):
        if peace.name == 'king' and peace.move and cell.field_name in ('C1', 'C8', 'G1', 'G8'):
            if cell.field_name in ('C1', 'C8'):
                rook = self.get_rook('right')
                self.moving(rook, self.get_straight_line_field(self.get_cell_king(self.queue), 3))
                rook.move_to_cell(
                    self.get_straight_line_field(self.get_cell_king(self.queue), 3))
            else:
                self.get_rook('left').move_to_cell(
                    self.get_straight_line_field(self.get_cell_king(self.queue), 4))

    def mode_king(self, cell, free_cells):
        for i in range(1, 5):
            new_cell = cell
            if self.get_straight_line_field(new_cell, i) is not None:
                if self.Check_castling(True) and i == 3:  # условие ракировки
                    for j in range(2):
                        new_cell = self.get_straight_line_field(new_cell, 3)
                        free_cells.add(new_cell)
                elif self.Check_castling(False) and i == 4:
                    for j in range(2):
                        new_cell = self.get_straight_line_field(new_cell, 4)
                        free_cells.add(new_cell)
                else:
                    new_cell = self.get_straight_line_field(new_cell, i)
                    if self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).color == self.queue:
                        pass
                    else:
                        free_cells.add(new_cell)
        for i in range(1, 5):
            new_cell = cell
            if self.get_diagonal_field(new_cell, i) is not None:
                new_cell = self.get_diagonal_field(new_cell, i)
                if self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).color == self.queue:
                    pass
                else:
                    free_cells.add(new_cell)

    def find_free_cells(self, cell, name: str, mode=None):
        if mode is None:
            free_cells = self.all_free_cells
        else:
            free_cells = self.possible_moves
        if name == 'rook':
            self.straight_move(cell, free_cells)

        elif name == 'bishop':
            self.diagonal_move(cell, free_cells)

        elif name == 'queen':
            self.straight_move(cell, free_cells)
            self.diagonal_move(cell, free_cells)

        elif name == 'king':
            self.mode_king(cell, free_cells)

        elif name == 'knight':
            for i in range(1, 9):
                new_cell = cell
                if self.get_g_field(new_cell, i) is not None:
                    new_cell = self.get_g_field(new_cell, i)
                    if not self.check_pieces_on_cell(new_cell):
                        free_cells.add(new_cell)
                    elif self.check_pieces_on_cell(new_cell) and self.get_piece_on_cell(new_cell).color != self.queue:
                        free_cells.add(new_cell)

        elif name == 'pawn':
            new_cell = cell
            self.pawn_move(new_cell, free_cells)
            self.pawn_killed(cell, free_cells)

        elif name == 'pawn1':
            new_cell = cell
            self.pawn_killed(cell, free_cells)
            for i in range(2):
                new_cell = self.pawn_move(new_cell, free_cells)


    def pawn_transformation(self, cell):
        self.get_piece_on_cell(cell).kill()
        peace = self.create_piece('Q' if self.queue == 'w' else 'q', cord=cell.field_name)
        peace.rect = cell.rect.copy()
        self.all_pieces.add(peace)
        print(peace.name)

    def drag(self, position: tuple):
        """Отвечает за анимацию перемещения фигуры курсором"""
        if self.dragged_piece is not None:
            cell = self.get_cell(position)
            if cell is not None:
                piece = self.get_piece_on_cell(cell)
                if self.designated_cell != cell:
                    self.unpick_cell()
                    if piece is None or cell == self.get_cell(self.down_position):
                        self.mark_cell(cell)
                    elif piece.color != self.get_piece_on_cell(self.pressed_cell).color:
                        self.mark_cell(cell, 2)
                    self.draw_playboard()
                    self.mark_free_fields()
                self.pick_cell(self.get_cell(self.down_position))
                self.designated_cell = self.get_cell(position)
            else:
                self.unpick_cell()
                self.draw_playboard()
            self.dragged_piece.rect.center = position
            self.grand_update()


    def btn_down(self, button_type: int, position: tuple):
        """производит действия при нажатии мыши"""
        self.down_position = position
        self.pressed_cell = self.get_cell(position)
        try:
            self.dragged_piece = self.get_piece_on_cell(self.pressed_cell)
            if self.dragged_piece.color == self.queue:
                self.get_all_free_cells_for_piece(self.dragged_piece)
                if self.dragged_piece != self.old_piece:
                    self.all_free_cells.empty()
                    self.all_attack_cells.empty()
                    self.get_all_free_cells_for_piece(self.dragged_piece)
                    self.unpick_cell()
                    self.pick_cell(self.get_cell(self.down_position))
                self.drag(position)
            else:
                self.dragged_piece = None
        except:
            self.dragged_piece = None

    def btn_up(self, button_type: int, position: tuple):
        """Производит действия при отпускании мыши"""
        relseased_cell = self.get_cell(position)
        if button_type == 3:
            self.queue = 'w' if self.queue == 'b' else 'b'
            self.unpick_cell()
        if button_type == 1:
            if relseased_cell is not None and relseased_cell == self.pressed_cell:
                self.pick_cell(relseased_cell)
        if self.dragged_piece is not None:
            try:
                self.move_peace(position)
            except AttributeError:
                self.dragged_piece.return_pieces(self.get_cell(self.down_position))
                self.get_all_free_cells_for_piece(self.dragged_piece)
                self.dragged_piece = None
                self.pick_cell(self.get_cell(self.down_position))
        self.draw_playboard()
        self.grand_update()

    def grand_update(self):
        self.all_cells.draw(self.__screen)
        self.all_areas.draw(self.__screen)
        self.all_pieces.draw(self.__screen)
        pygame.display.update()

    def put_into_place(self):
        self.unpick_cell()
        self.dragged_piece.return_pieces(self.get_cell(self.down_position))
        self.get_all_free_cells_for_piece(self.get_cell(self.down_position))
        self.pick_cell(self.get_cell(self.down_position))

    def piece_move(self, piece, put_piece, cell):
        if piece is not None and piece.color != self.queue:
            piece.kill()
        put_piece.move_to_cell(cell)
        self.castling(cell, put_piece)
        put_piece.move = False
        if put_piece.name == 'pawn' and cell.field_name[1] in ('1', '8'):
            self.pawn_transformation(cell)
        self.unpick_cell()
        self.Queue()
        self.all_free_cells.empty()
        self.all_attack_cells.empty()

    def move_peace(self, position):
        relseased_cell = self.get_cell(position)
        piece = self.get_piece_on_cell(relseased_cell)
        if self.dragged_piece.field_name != relseased_cell.field_name and self.check_cell_in_grope_cell(
                relseased_cell, self.all_free_cells):
            self.piece_move(piece, self.dragged_piece, relseased_cell)
            self.dragged_piece = None
        else:
            self.put_into_place()
        if not self.check_shah():
            print('шаха нет')
        else:
            print("шах")

    def mark_cell(self, cell, col: int = 0):
        mark = Area(cell, col)
        self.all_areas.add(mark)

    def pick_cell(self, cell):
        piece = self.get_piece_on_cell(cell)
        if self.picked_piece is None:
            if piece is not None and piece.color == self.queue:
                pick = Area(cell, 1)
                self.all_areas.add(pick)
                self.picked_piece = piece
                self.picked_cell = cell
        else:
            if self.picked_piece.field_name != cell.field_name and self.check_cell_in_grope_cell(cell, self.all_free_cells):
                self.moving(self.picked_piece, cell)
                self.piece_move(piece, self.picked_piece, cell)

    def moving(self, piece, cell):
        """Отвечает за анимацию передвижения фигуры"""
        while piece.rect.center != cell.rect.center:
            piece.moving_piece(piece.rect.center, cell.rect.center)
            self.grand_update()

    def unpick_cell(self):
        self.picked_piece = None
        self.picked_cell = None
        self.all_areas.empty()

    def Queue(self):
        self.queue = 'b' if self.queue == 'w' else 'w'

class Cell(pygame.sprite.Sprite):
    def __init__(self, color_index: int, size: int, coords: tuple, name: str):
        super().__init__()
        x, y = coords
        self.coords = coords
        self.color = color_index
        self.field_name = name
        self.image = pygame.image.load(IMG_PATH + COLORS[color_index])
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = pygame.Rect(x * size, y * size, size, size)
        self.mark = False

class Area(pygame.sprite.Sprite):
    def __init__(self, cell: Cell, type_of_area: int = 0):
        super().__init__()
        coords = (cell.rect.x, cell.rect.y)
        area_size = (cell.rect.width, cell.rect.height)
        if type_of_area == 0:
            picture = pygame.image.load(IMG_PATH + 'select_field.png').convert_alpha()
            self.image = pygame.transform.scale(picture, area_size)
        elif type_of_area == 1:
            self.image = pygame.Surface(area_size).convert_alpha()
            self.image.fill(ACTIV_CELL_COLOR)
        if type_of_area == 2:
            picture = pygame.image.load(IMG_PATH + 'select_field_red.png').convert_alpha()
            self.image = pygame.transform.scale(picture, area_size)
        if type_of_area == 3:
            picture = pygame.image.load(IMG_PATH + 'possible_move.png').convert_alpha()
            self.image = pygame.transform.scale(picture, area_size)
        if type_of_area == 4:
            picture = pygame.image.load(IMG_PATH + 'circle.png').convert_alpha()
            self.image = pygame.transform.scale(picture, area_size)
        self.rect = pygame.Rect(coords, area_size)
        self.field_name = cell.field_name
