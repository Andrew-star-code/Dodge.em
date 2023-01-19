import random
fullEscape = 5

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
