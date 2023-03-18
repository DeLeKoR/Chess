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
        self.__sound = pygame.mixer.Sound('sound/move.mp3')

    def move_to_cell(self, cell):
        if self.field_name != cell.field_name:
            print(self.field_name, cell.field_name)
            self.field_name = cell.field_name
            self.__sound.set_volume(0.4)
            self.__sound.play()
            board_data.history.append([self.field_name, cell.field_name])
        self.rect = cell.rect.copy()
        print(6)

    def return_pieces(self, cell):
        self.rect = cell.rect.copy()


class King(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_king.png')
        self.name = 'king'


class Queen(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_queen.png')
        self.name = 'queen'


class Rook(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_rook.png')
        self.name = 'rook'


class Bishop(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_bishop.png')
        self.name = 'bishop'


class Knight(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_knight.png')
        self.name = 'knight'


class Pawn(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_pawn.png')
        self.name = 'pawn'


