import pygame as p
import tkinter as tk
from tkinter import messagebox
import random
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from AuthWindow import Ui_MainWindow
import numpy as np
import sys

# Конфигурация
WIDTH = HEIGHT = 512
DIMENSION = 7
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
fullEscape = 5

# Окно авторизации
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

# Всплывающие оповещения
def message(text):
    msg = QMessageBox()
    msg.setWindowTitle("Оповещение")
    msg.setText(text)
    msg.exec()

# Шифрование
def Encrypt(word):
    word = list(word)
    key = 7
    word = np.array(word)
    pass_len = len(word)
    matrix = np.full((5 + key, key), ' ')
    flag = 0
    for i in range(5 + key):
        for j in range(key):
            if flag < pass_len:
                matrix[i][j] = word[flag]
                flag += 1

    matrix = matrix.transpose()
    result = ""
    for i in range(key):
        for j in range(5 + key):
            result += matrix[i][j]
    return result

# Дешифрование
def Decipher(word):
    word = list(word)
    key = 7
    pass_len = len(word)
    matrix = np.full((key, 5 + key), ' ')
    flag = 0
    for i in range(key):
        for j in range(5 + key):
            if flag < pass_len:
                matrix[i][j] = word[flag]
                flag += 1
    matrix = matrix.transpose()
    result = ""
    for i in range(5 + key):
        for j in range(key):
            result += matrix[i][j]
    return result

# Считывание логина и пароля
def log():
    log = ui.plainTextEditLog.toPlainText()
    return log
def pas():
    pas = ui.plainTextEditPass.toPlainText()
    return pas

# Очистка полей логина и пароля
def clear():
    ui.plainTextEditLog.setPlainText("")
    ui.plainTextEditPass.setPlainText("")

# Авторизации + работа личного кабинета
def click_auth():
    with open('credentials.txt', 'r') as f:
        flag = 0
        credentials = log() + pas()
        for row in f:
            if row == Encrypt(credentials) + "\n":
                flag = 1
                break
    clear()
    if flag == 1:
        MainWindow.close()
        main()
    else:
        message("Неверный логин или пароль, попробуйте еще раз")

# Регистрация
def click_reg():
    with open('login.txt', 'r') as f:
        for row in f:
            flag = 0
            if (Encrypt(log()) + "\n") == row:
                message("Такой логин уже существует")
                flag = 1
                break
        if flag == 0:
            checkLog = len(log())
            checkPas = len(pas())
            if checkLog < 16 and checkLog > 4 and checkPas < 16 and checkPas > 4:
                space = " "
                if space in log() or space in pas():
                    message("Недопустимый символ в логине или пароле: Пробел")
                else:
                    with open('login.txt', 'a') as f:
                        f.write(Encrypt(log()) + "\n")
                    with open('credentials.txt', 'a') as d:
                        credentials = log() + pas()
                        d.write(Encrypt(credentials) + '\n')
                    clear()
            else:
                message("Некорректные логин или пароль, попробуйте еще раз")

ui.pushButtonRegistration.clicked.connect(click_reg)
ui.pushButtonLogin.clicked.connect(click_auth)


# Подгрузка изображений
def loadImages():
    pieces = ["wp", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# Состояние игры
class GameState:
    def __init__(self):
        self.board = [
            ["--", "wp", "wp", "wp", "wp", "wp", "--"],
            ["--", "--", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "bp"],
            ["--", "--", "--", "--", "--", "--", "--"],
        ]

        self.whiteToMove = True # Текущий ход
        self.moveLog = [] # История ходов
        self.gameOver = False # Переменная окончания игры
        self.whiteScore = 0 # Очки белых
        self.blackScore = 0 # Очки черных
        self.pieceEscaped = False # Отслеживание сбегающих шашек
        self.moveForward = False # Отслеживание результативных ходов

    # Получение допустимых ходов
    def getValidMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    self.getPieceMoves(r, c, moves)
        return moves

    # Получение ходов фигуры
    def getPieceMoves(self, r, c, moves):
        if self.whiteToMove:
            if r + 1 <= 7:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
            if c + 1 <= 6:
                if self.board[r][c + 1] == "--":
                    moves.append(Move((r, c), (r, c + 1), self.board))
            if c - 1 >= 1:
                if self.board[r][c - 1] == "--":
                    moves.append(Move((r, c), (r, c - 1), self.board))

        else:
            if c - 1 >= 0:
                if self.board[r][c - 1] == "--":
                    moves.append(Move((r, c), (r, c - 1), self.board))
            if r + 1 <= 5:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
            if r - 1 >= 0:
                if self.board[r - 1][c] == "--":
                    moves.append(Move((r, c), (r - 1, c), self.board))


    # Пробный ход
    def testMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.isPieceEscape:
            self.board[move.endRow][move.endCol] = "--"
            self.pieceEscaped = True
        if move.isMoveForward:
            self.moveForward = True

    # Ход игрока
    def makePlayerMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.isPieceEscape:
            self.board[move.endRow][move.endCol] = "--"
            if self.whiteToMove:
                self.blackScore += 1
                if self.blackScore == 5:
                    self.gameOver = True
            else:
                self.whiteScore += 1
                if self.whiteScore == 5:
                    self.gameOver = True


    # Ход компьютера
    def makeComputerMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.isPieceEscape:
            self.board[move.endRow][move.endCol] = "--"
            if self.whiteToMove:
                self.blackScore += 1
                if self.blackScore == 5:
                    self.gameOver = True
            else:
                self.whiteScore += 1
                if self.whiteScore == 5:
                    self.gameOver = True


    # Удаление последнего хода
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = "--"
            self.whiteToMove = not self.whiteToMove


class Move():
    ranksToRows = {"1": 6, "2": 5, "3": 4, "4": 3, "5": 2, "6": 1, "7": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.isPieceEscape = False
        self.isMoveForward = False
        if (self.pieceMoved == 'wp' and self.endRow == 6) or (self.pieceMoved == 'bp' and self.endCol == 0):
            self.isPieceEscape = True
        if (self.pieceMoved == 'wp' and self.endRow > self.startRow) or (self.pieceMoved == 'bp' and self.endCol < self.startCol):
            self.isMoveForward = True
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    # Переопределение метода equals для правильного сравнения ходов
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    # Получение координат по нотации Эдвардса
    def getBoardNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

# Основной цикл
def main():
    p.init()
    p.display.set_caption('Компьютерная логическая игра "Доджем"')
    p.display.set_icon(p.image.load("images/icon.png"))
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    firstPlayer = True
    secondPlayer = False
    while running:
        humanTurn = (gs.whiteToMove and firstPlayer) or (not gs.whiteToMove and secondPlayer)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gs.gameOver and humanTurn:
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
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            gs.makePlayerMove(move)
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]

        if not gs.gameOver and not humanTurn:
            computerMove = findOptimalMove(gs, validMoves)
            if computerMove is not None:
                gs.makeComputerMove(computerMove)
                gs.pieceEscaped = False
                gs.moveForward = False
                moveMade = True
            else:
                moveMade = True


        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()

        # Вывод уведомления об окончании игры
        if gs.gameOver:
            if gs.whiteToMove:
                msg_box = tk.messagebox.askquestion('Победа Черных',
                                                    'Выйти из приложения?',
                                                    icon='warning')
                if msg_box == 'yes':
                    p.display.quit()
                    p.quit()
                else:
                    gs = GameState()
                    validMoves = gs.getValidMoves()
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
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False

# Выделение квадратов с доступными ходами
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(50)
            s.fill(p.Color('Blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color("Yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

# Нахождение оптимального хода для компьютера
def findOptimalMove(gs, validMoves):
    score = 0
    maxScore = -fullEscape
    bestMove = None
    moves = validMoves
    random.shuffle(moves)
    for playerMove in moves:
        gs.testMove(playerMove)
        if gs.moveForward:
            score = 1
        if gs.pieceEscaped:
            score = 2
        if gs.gameOver:
            score = fullEscape
        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    return bestMove

# Отрисовка графики при текущем состоянии игры
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

# Отрисовка игровой доски
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Отрисовка фигур
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



sys.exit(app.exec())

