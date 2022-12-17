import pygame as pg
from game_config import *

class Piece(pg.sprite.Sprite):
    def __init__(self, cell_size: int, color: str, field_name: str, file_posfix: str):
        super().__init__()
        picture = pg.image.load(PIECE_PATH + color + file_posfix)
        self.image = pg.transform.scale(picture, (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self._color = color
        self.field_name = field_name

class Rook(Piece):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_rook.png')

class Empty(Piece):
    def __init__(self, cell_size: int, color: str, field: str):
        super().__init__(cell_size, color, field, '_empty.png')
