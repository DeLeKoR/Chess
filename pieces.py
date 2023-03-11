import pygame
from options import *

class Pieces(pygame.sprite.Sprite):
    def __init__(self, cell_size: int, color: str, field_name: str, file_posfix: str):
        super().__init__()
        picture = pygame.image.load(PIECES_PATH + color + file_posfix).convert_alpha()
        self.image = pygame.transform.scale(picture, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self._color = color
        self.field_name = field_name

class King(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_king.png')


class Queen(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_queen.png')


class Rook(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_rook.png')


class Bishop(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_bishop.png')


class Knight(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_knight.png')


class Pawn(Pieces):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_pawn.png')


