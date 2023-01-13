import pygame as p
import tkinter as tk
from tkinter import messagebox
import Engine


WIDTH = HEIGHT = 512
DIMENSION = 7
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["wp", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    p.display.set_caption('Компьютерная логическая игра "Доджем"')
    p.display.set_icon(p.image.load("images/icon.png"))
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gs.gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()

        if gs.gameOver:
            if gs.whiteToMove:
                msg_box = tk.messagebox.askquestion('Победа Черных',
                                                    'Выйти из приложения?',
                                                    icon='warning')
                if msg_box == 'yes':
                    p.display.quit()
                    p.quit()
                else:
                    gs = Engine.GameState()
                    validMoves= gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False

            else:
                msg_box = tk.messagebox.askquestion('Победа Белых',
                                                    'Выйти из приложения?',
                                                    icon='warning')
                if msg_box == 'yes':
                    p.display.quit()
                    p.quit()
                else:
                    p.display.set_caption('Компьютерная логическая игра "Доджем"')
                    gs = Engine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False




def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(50)
            s.fill(p.Color('Blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))



def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




if __name__ == "__main__":
    main()
