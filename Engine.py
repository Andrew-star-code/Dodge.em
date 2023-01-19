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


    # Функция пробного хода
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

    # Функция хода игрока
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


    # Функция хода компьютера
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


    # Функция удаления последнего хода
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