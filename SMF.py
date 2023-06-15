import random

pieceScore = {"K": 0, "Q":10, "R":5, "B":3,"N":3, "p":1}

knightScores = [[ 1, 1, 1, 1, 1, 1, 1, 1],
                [ 1, 2, 2, 2, 2, 2, 2, 1],
                [ 1, 2, 3, 3, 3, 3, 2, 1],
                [ 1, 2, 3, 4, 4, 3, 2, 1],
                [ 1, 2, 3, 4, 4, 3, 2, 1],
                [ 1, 2, 3, 3, 3, 3, 2, 1],
                [ 1, 2, 2, 2, 2, 2, 2, 1],
                [ 1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[ 4, 3, 2, 1, 1, 2, 3, 4],
                [ 3, 4, 3, 2, 2, 3, 4, 3],
                [ 2, 3, 4, 3, 3, 4, 3, 2],
                [ 1, 2, 3, 4, 4, 3, 2, 1],
                [ 1, 2, 3, 4, 4, 3, 2, 1],
                [ 2, 3, 4, 3, 3, 4, 3, 2],
                [ 3, 4, 3, 2, 2, 3, 4, 3],
                [ 4, 3, 2, 1, 1, 2, 3, 4]]

queenScore =   [[ 1, 1, 1, 3, 1, 1, 1, 1],
                [ 1, 2, 3, 3, 3, 1, 1, 1],
                [ 1, 4, 3, 3, 3, 4, 2, 1],
                [ 1, 2, 3, 3, 3, 3, 2, 1],
                [ 1, 2, 3, 3, 3, 3, 2, 1],
                [ 1, 4, 3, 3, 3, 4, 2, 1],
                [ 1, 1, 2, 3, 3, 1, 1, 1],
                [ 1, 1, 1, 3, 1, 1, 1, 1]]

rookScore =    [[ 4, 3, 4, 4, 4, 4, 3, 4],
                [ 4, 4, 4, 4, 4, 4, 4, 4],
                [ 1, 1, 2, 3, 3, 2, 1, 1],
                [ 1, 2, 3, 4, 4, 3, 2, 1],
                [ 1, 2, 3, 4, 4, 3, 2, 1],
                [ 1, 1, 2, 2, 2, 2, 1, 1],
                [ 4, 4, 4, 4, 4, 4, 4, 4],
                [ 4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScore =   [[ 8, 8, 8, 8, 8, 8, 8, 8],
                    [ 8, 8, 8, 8, 8, 8, 8, 8],
                    [ 5, 6, 6, 7, 7, 6, 6, 5],
                    [ 2, 3, 3, 5, 5, 3, 3, 2],
                    [ 1, 2, 3, 4, 4, 3, 2, 1],
                    [ 1, 1, 2, 3, 3, 2, 1, 1],
                    [ 1, 1, 1, 0, 0, 1, 1, 1],
                    [ 0, 0, 0, 0, 0, 0, 0, 0]]


blackPawnScore =   [[ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 1, 1, 1, 0, 0, 1, 1, 1],
                    [ 1, 1, 2, 3, 3, 2, 1, 1],
                    [ 1, 2, 3, 4, 4, 3, 2, 1],
                    [ 2, 3, 3, 5, 5, 3, 3, 2],
                    [ 5, 6, 6, 7, 7, 6, 6, 5],
                    [ 8, 8, 8, 8, 8, 8, 8, 8],
                    [ 8, 8, 8, 8, 8, 8, 8, 8]]


piecePositionScores = {"Q": queenScore, "R": rookScore, "B": bishopScores,"N": knightScores, "bp": blackPawnScore, "wp": whitePawnScore}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

'''
Prende e restituisce una mossa random
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

'''
Trova la mossa migliore, Min max senza ricorsione
'''
def findBestMoveMinMaxNoRecursion(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.stalemate:
            opponentMaxScore = STALEMATE
        elif gs.checkmate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = -turnMultiplier * CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

'''
Metodo aiutante per effettuare la prima chiamata di ricorsione
'''
def findBestMove(gs, validMoves, returnQueue):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    returnQueue.put(nextMove)
    

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    #ordine delle mosse da implementare in seguito
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta: #mossa impossibile da contrastare o parare
            break
    return maxScore


'''
Punteggio positivo Vantaggio bianco, Punteggio negativo Vantaggio nero
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                #punteggio in base alla posizione
                piecePositionScore = 0
                if square[1] != "K":
                    if square[1] == "p": #per pedoni
                        piecePositionScore = piecePositionScores[square][row][col]
                    else: #per gli altri pezzi
                        piecePositionScore = piecePositionScores[square[1]][row][col]


                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * .1
                elif square[0] == 'b':
                    score -= pieceScore[square[1]]+ piecePositionScore * .1

    return score






'''
Punteggio della scacchiera basata sul materiale
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score