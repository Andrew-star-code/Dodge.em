import pygame as pg

FPS = 30
WINDOW_SIZE = (800, 800)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
CERULEAN = (156, 192, 231)
MID_GRAY = (90, 90, 90)
BACKGROUND = CERULEAN
CELL_QTY = 5
CELL_SIZE = 90
COLORS = ['white.jpg', 'black.jpg']
FNT_PATH = 'assets/fonts/Verdana.ttf'
FNT_SIZE = 18
LTRS = 'abcdefghijklmnopqrstuvwxyz'
IMG_PATH = 'assets/images/'
WIN_BG_IMG = 'backwindow.jpg'
PIECES_TYPES = {
    'r':('Rook', 'b'), 'R':('Rook', 'w'),
    '0':('Empty', 'b'),
}
PIECE_PATH = 'assets/pieces/'