from game_config import *
from game_items import *

clock = pg.time.Clock()
screen = pg.display.set_mode(WINDOW_SIZE)
screen.fill(BACKGROUND)

playboard = playboard(screen)

run = True
while run:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            playboard.btn_down(event.button, event.pos)
        if event.type == pg.MOUSEBUTTONUP:
            playboard.btn_up(event.button, event.pos)
