import pygame
import board_data
from options import *

class Pieces(pygame.sprite.Sprite):
    def __init__(self, cell_size: int, color: str, field_name: str, file_posfix: str):
        super().__init__()
        picture = pygame.image.load(PIECES_PATH + color + file_posfix).convert_alpha()
        self.image = pygame.transform.scale(picture, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.color = color
        self.field_name = field_name
        #self.all_free_cells = pygame.sprite.Group()
        self.__sound = pygame.mixer.Sound('sound/move.mp3')
        self.attack = False
        self.move = True
        self.velocity = 0.01

    def move_to_cell(self, cell):
        if self.field_name != cell.field_name:
            print(self.field_name, cell.field_name, '\n')
            self.field_name = cell.field_name
            self.__sound.set_volume(0.4)
            self.__sound.play()
            board_data.history.append([self.field_name, cell.field_name])
        self.rect = cell.rect.copy()

    def return_pieces(self, cell):
        self.rect = cell.rect.copy()

    def moving_piece(self, old_cell, new_cell):
        start_pos = old_cell
        end_pos = new_cell
        current_pos = (int(start_pos[0] + (end_pos[0] - start_pos[0]) * self.velocity),
                       int(start_pos[1] + (end_pos[1] - start_pos[1]) * self.velocity))
        self.rect.center = current_pos
        self.velocity += 0.075 if self.velocity < 0.9 else 0.015
        if self.rect.center == end_pos:
            self.velocity = 0.01



class King(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_king.png')
        self.name = 'king'
        self.value = None


class Queen(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_queen.png')
        self.name = 'queen'
        self.value = 9


class Rook(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_rook.png')
        self.name = 'rook'
        self.value = 5



class Bishop(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_bishop.png')
        self.name = 'bishop'
        self.value = 3



class Knight(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_knight.png')
        self.name = 'knight'
        self.value = 3



class Pawn(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_pawn.png')
        self.name = 'pawn'
        self.value = 1



