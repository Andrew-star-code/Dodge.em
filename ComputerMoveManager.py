import random
fullEscape = 1000
firstPlayer = True
secondPlayer = False

def findMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

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
            score = 5
        if gs.gameOver:
            score = fullEscape
        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    print(score)
    return bestMove
