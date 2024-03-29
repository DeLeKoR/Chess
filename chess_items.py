import pygame.image

from pieces import *
import board_data
pygame.init()
fnt_num = pygame.font.Font(pygame.font.get_default_font(), 24)

class Chessboard:
    def __init__(self,cell_qty=CELL_QTY, cell_size=size_field):
        pygame.display.set_caption("Шахматы")
        self.__screen = pygame.display.set_mode((WINDOW_SIZE))
        self.__table = board_data.board
        self.__qty = cell_qty
        self.__size = cell_size
        self.__pieces_types = PIECES_TYPES
        self.__all_cells = pygame.sprite.Group()
        self.__all_pieces = pygame.sprite.Group()
        self.__all_areas = pygame.sprite.Group()
        self.__pressed_cell = None
        self.__picked_piece = None
        self.__dragged_piece = None
        self.__old_position = None
        self.__old_piece = None
        self.__draw_playboard()
        self.__setup_board()
        self.__grand_update()
        self.queue = 'w'
    def __draw_playboard(self):
        self.__screen.fill(BACKGROUND)
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
        self.__aplly_offset_for_cells(cell_offset)

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

    def __aplly_offset_for_cells(self, offset):
        for cell in self.__all_cells:
            cell.rect.x += offset[0]
            cell.rect.y += offset[1]

    def __setup_board(self):
        for j, row in enumerate(self.__table):
            for i, field_value in enumerate(row):
                if field_value != 0:
                    piece = self.__create_piece(field_value, (j, i))
                self.__all_pieces.add(piece)
        for piece in self.__all_pieces:
            for cell in self.__all_cells:
                if piece.field_name == cell.field_name:
                    piece.rect = cell.rect.copy()

    def __create_piece(self, piece_symbol: str, table_coord: tuple):
        field_name = self.__to_field_name(table_coord)
        piece_tuple = self.__pieces_types[piece_symbol]
        classname = globals()[piece_tuple[0]]
        return classname(self.__size, piece_tuple[1], field_name)

    def __to_field_name(self, table_coord: tuple):
        return LTRS[table_coord[1]] + str(self.__qty - table_coord[0])

    def __get_piece(self, position: tuple):
        for piece in self.__all_pieces:
            if piece.rect.collidepoint(position):
                return piece
        return None

    def __get_cell(self, position: tuple):
        for cell in self.__all_cells:
            if cell.rect.collidepoint(position):
                return cell
        return None

    def __get_piece_on_cell(self, cell):
        for piece in self.__all_pieces:
            if piece.field_name == cell.field_name:
                return piece
        return None

    def __check_pieces_on_cell(self, cell):
        piece = self.__get_piece_on_cell(cell)
        if piece is not None and piece.color == self.queue:
            print(True)
            return True
        else:
            print(False)
            return False

    def drag(self, position: tuple):
        """Отвечает за анимацию перемещения фигуры курсором"""
        if self.__dragged_piece is not None:
            self.__dragged_piece.rect.center = position
            self.__grand_update()

    def btn_down(self, button_type: int, position: tuple):
        """производит действия при нажатии мыши"""
        self.old_position(position)
        self.__pressed_cell = self.__get_cell(position)
        try:
            self.__dragged_piece = self.__get_piece_on_cell(self.__pressed_cell)
            if self.__dragged_piece.color == self.queue:
                if self.__dragged_piece != self.__old_piece:
                    self.__unpick_cell(self.__pressed_cell)
                self.drag(position)
            else:
                self.__dragged_piece = None
        except:
            self.__dragged_piece = None

    def btn_up(self, button_type: int, position: tuple):
        """производит действия при отпускании мыши"""
        relseased_cell = self.__get_cell(position)
        if (relseased_cell is not None) and (relseased_cell == self.__pressed_cell):
            if button_type == 3:
                self.__mark_cell(relseased_cell)
            if button_type == 1:
                self.pick_cell(relseased_cell)
            if button_type == 6:
                self.__unmark_all_cells()
        if self.__dragged_piece is not None:
            try:
                self.__move_peace(position)
            except AttributeError:
                self.__dragged_piece.return_pieces(self.__get_cell(self.__old_position))
                self.__dragged_piece = None
        self.__grand_update()

    def __grand_update(self):
        self.__draw_playboard()
        self.__all_cells.draw(self.__screen)
        self.__all_areas.draw(self.__screen)
        self.__all_pieces.draw(self.__screen)
        pygame.display.update()

    def __move_peace(self, position):
        relseased_cell = self.__get_cell(position)
        piece = self.__get_piece_on_cell(relseased_cell)
        if self.__dragged_piece.field_name != relseased_cell.field_name:
            if self.__check_pieces_on_cell(relseased_cell):
                self.__dragged_piece.return_pieces(self.__get_cell(self.__old_position))
                self.__dragged_piece = None
            else:
                if piece is not None and piece.color != self.queue:
                    piece.kill()
                self.__dragged_piece.move_to_cell(relseased_cell)
                self.__dragged_piece = None
                self.__picked_piece = None
                self.__unmark_all_cells()
                self.Queue()
        else:
            self.__dragged_piece.return_pieces(relseased_cell)
            self.__dragged_piece = None
            self.pick_cell(relseased_cell)

    def __mark_cell(self, cell):
        if not cell.mark:
            mark = Area(cell)
            self.__all_areas.add(mark)
        else:
            for area in self.__all_areas:
                if area.field_name == cell.field_name:
                    area.kill()
                    break
        cell.mark ^= True

    def pick_cell(self, cell):
        piece = self.__get_piece_on_cell(cell)
        if self.__picked_piece is None:
            if piece is not None and piece.color == self.queue:
                pick = Area(cell, False)
                self.__all_areas.add(pick)
                self.__picked_piece = piece
        else:
            if self.__check_pieces_on_cell(cell):
                pass
            elif self.__picked_piece.field_name != cell.field_name:
                if piece is not None and piece.color != self.queue:
                    piece.kill()
                self.__picked_piece.move_to_cell(cell)
                self.__unpick_cell(cell)
                self.Queue()
            else:
                self.__unpick_cell(cell)

    def __unpick_cell(self, cell):
        self.__picked_piece = None
        self.__unmark_all_cells()


    def __unmark_all_cells(self):
        self.__all_areas.empty()
        for cell in self.__all_cells:
            cell.mark = False


    def old_position(self, position):
        self.__old_position = position

    def Queue(self):
        self.queue = 'b' if self.queue == 'w' else 'w'


class Cell(pygame.sprite.Sprite):
    def __init__(self, color_index: int, size: int, coords: tuple, name: str):
        super().__init__()
        x, y = coords
        self.color = color_index
        self.field_name = name
        self.image = pygame.image.load(IMG_PATH + COLORS[color_index])
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = pygame.Rect(x * size, y * size, size, size)
        self.mark = False

class Area(pygame.sprite.Sprite):
    def __init__(self, cell: Cell, type_of_area: bool = True):
        super().__init__()
        coords = (cell.rect.x, cell.rect.y)
        area_size = (cell.rect.width, cell.rect.height)
        if type_of_area:
            picture = pygame.image.load(IMG_PATH + 'circle.png').convert_alpha()
            self.image = pygame.transform.scale(picture, area_size)
        else:
            self.image = pygame.Surface(area_size).convert_alpha()
            self.image.fill(ACTIV_CELL_COLOR)
        self.rect = pygame.Rect(coords, area_size)
        self.field_name = cell.field_name
