class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunction = {'p':self.getPownMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves, 'B':self.getBishopMoves, "Q":self.getQueenMoves, "K":self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkmate = False
        self.stalemate = False
        self.enPassantPossible=()
        self.enPassantPossibleLog=[self.enPassantPossible]
        self.currentCastlingRight = CastleRights(True,True,True,True)
        self.castleRightLog = [CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]
        self.in_Check = False
        self.pins = [] #pezzi inchiodati
        self.checks = [] #Scacco

        


    #Prende e esegue mosse (non funziona l'arrocco, promozione e en-passant)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        #aggiornare la posizione dei re
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #promozione
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0]+'Q'
        
        # en passant
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = '--'
            
        #update enPassantPossible
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enPassantPossible=()

        #mossa arrocco
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #arrocco corto
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] # muove la torre
                self.board[move.endRow][move.endCol+1] = '--' # spazio vuoto
            else: #arrocco lungo
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] # muove la torre
                self.board[move.endRow][move.endCol-2] = '--' # spazio vuoto
    
        self.enPassantPossibleLog.append(self.enPassantPossible)

        #update arrocco - ogni volta che si muove o la torre R o il re K
        self.updateCastleRight(move)
        self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,self.currentCastlingRight.wqs,self.currentCastlingRight.bqs))

    


    #undo move (annulla mossa)
    def undoMove(self):
        if len(self.moveLog)!=0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo en passant
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            
            self.enPassantPossibleLog.pop()
            self.enPassantPossible = self.enPassantPossibleLog[-1]

            #undo arrocco
            self.castleRightLog.pop() # elimina il nuovo arrocco dalla mossa cancellata 
            newRight  = self.castleRightLog[-1] #setta l'arrocco corrente con l'ultimo della lista
            self.currentCastlingRight = CastleRights(newRight.wks,newRight.bks,newRight.wqs,newRight.bqs)
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #arrocco corto
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1] # muove la torre
                    self.board[move.endRow][move.endCol-1] = '--' # spazio vuoto
                else: #arrocco lungo
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1] # muove la torre
                    self.board[move.endRow][move.endCol+1] = '--' # spazio vuoto
            self.checkmate = False
            self.stalemate = False
    
        
    def updateCastleRight(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7: #torre di sinistra
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0: #torre di sinistra
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False
        
        #se la torre è catturata
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False

    #controllo validità mossa
    def getValidMoves(self):
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        # advanced algorithm
        moves = []
        self.in_Check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.whiteToMove:
            king_row = self.whiteKingLocation[0]
            king_col = self.whiteKingLocation[1]
        else:
            king_row = self.blackKingLocation[0]
            king_col = self.blackKingLocation[1]
        if self.in_Check:
            if len(self.checks) == 1:  #solo uno scacco, bloccare il pezzo o spostare il re
                moves = self.getAllPossiblesMoves() # to block the check you must put a piece into one of the squares between the enemy piece and your king
                check = self.checks[0]  # check information
                checkRow = check[0]
                checkCol = check[1]
                piece_checking = self.board[checkRow][checkCol]
                valid_squares = []  # squares that pieces can move to
                # if knight, must capture the knight or move your king, other pieces can be blocked
                if piece_checking[1] == "N":
                    valid_squares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)  # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == checkRow and valid_square[1] == checkCol:  # once you get to piece and check
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # iterate through the list backwards when removing elements
                    if moves[i].pieceMoved[1] != "K":  # move doesn't move king so it must block or capture
                        if not (moves[i].endRow,
                                moves[i].endCol) in valid_squares:  # move doesn't block or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.getKingMoves(king_row, king_col, moves)
        else:  # not in check - all moves are fine
            moves = self.getAllPossiblesMoves()
            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
            else:
                self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.currentCastlingRight = tempCastleRights
        return moves


    #Determina se il bianco è sotto scacco
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    #Determina se l'avversario può attaccare il quadrato r,c
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossiblesMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False


    #Tutte le mosse (senza considerare gli scacchi)
    def getAllPossiblesMoves(self):
        moves = []
        for r in range(len(self.board)): #riga
            for c in range(len(self.board[r])): #colonna
                turn = self.board[r][c][0] #prende il primo carattere di quella casella
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove): 
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r,c,moves)
        return moves


    def checkForPinsAndChecks(self):
        pins = []  # quadrati inchiodati
        checks = []  # quandrati dove l'avversario fa scacco
        in_Check = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possiblePin = ()  # reset possibile inchiodatura
            for i in range(1, 8):
                endRow = startRow + direction[0] * i
                endCol = startCol + direction[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K":
                        if possiblePin == ():  # primo pezzo alleato potrebbe essere inchiodato
                            possiblePin = (endRow, endCol, direction[0], direction[1])
                        else:  # secondo pezzo alleato - no check o inchiodature da quasta direzione
                            break
                    elif endPiece[0] == enemyColor:
                        enemyType = endPiece[1]
                        # 5 possibili situazioni
                        # 1.) king e rook
                        # 2.) king e bishop
                        # 3.) 1 quadrato in diagonale king e pawn
                        # 4.) qualsiasi direzione King e queen
                        # 5.) qualsiasi direzione un quandreto di distanza king e king
                        if (0 <= j <= 3 and enemyType == "R") or (4 <= j <= 7 and enemyType == "B") or (i == 1 and enemyType == "p" and ((enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or (enemyType == "Q") or (i == 1 and enemyType == "K"):
                            if possiblePin == ():  # nessun pezzo blocca, allora è scacco
                                in_Check = True
                                checks.append((endRow, endCol, direction[0], direction[1]))
                                break
                            else:  # pezzo che blocca, quindi inchiodatura
                                pins.append(possiblePin)
                                break
                        else:  # nessun pezzo sta facendo scacco
                            break
                else:
                    break  # fuori
        # scacco di cavallo
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            endRow = startRow + move[0]
            endCol = startCol + move[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N":  # il cavallo nemico attacca il re
                    in_Check = True
                    checks.append((endRow, endCol, move[0], move[1]))
        return in_Check, pins, checks
        
                    
    def getPownMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            enemyColor = "b"
            kingRow, kingCol = self.whiteKingLocation
        else:
            moveAmount = 1
            startRow = 1
            enemyColor = "w"
            kingRow, kingCol = self.blackKingLocation
        
        if self.board[r+moveAmount][c] == "--":
            if not piecePinned or pinDirection == (moveAmount, 0):
                moves.append(Move((r,c), (r+moveAmount,c), self.board))
                if r == startRow and self.board[r+2*moveAmount][c] == "--":
                    moves.append(Move((r,c), (r+2*moveAmount,c), self.board))

            #cattura
        if c-1 >= 0: #cattura a sinistra
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r+moveAmount][c-1][0] == enemyColor:
                    # if not piecePinned or pinDirection == (-1, -1):
                    moves.append(Move((r,c), (r+moveAmount,c-1), self.board))
                elif (r+moveAmount, c-1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c: #il re è alla sinistra del pedone
                            #tra re e pedonte oppure fuori dal raggio di azione, tra pawn e board
                            insideRange = range(kingCol + 1, c-1)
                            outsideRange = range(c+1, 8)
                        else: #il re è a destra del pedone
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c-2,-1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r,c),(r+moveAmount,c-1), self.board, isEnPassantMove=True))
        if c+1 <= 7: #cattura a destra
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r+moveAmount][c+1][0] == enemyColor:
                    # if not piecePinned or pinDirection == (-1, 1):
                    moves.append(Move((r,c), (r+moveAmount,c+1), self.board))
                elif (r+moveAmount, c+1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c: #il re è alla sinistra del pedone
                            #tra re e pedonte oppure fuori dal raggio di azione, tra pawn e board
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c+2, 8)
                        else: #il re è a destra del pedone
                            insideRange = range(kingCol - 1, c +1 , -1)
                            outsideRange = range(c-1,-1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r,c),(r+moveAmount,c+1), self.board, isEnPassantMove=True))



    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1,0),(0,-1),(1,0),(0,1))#up left down right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[0]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break



    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2,-1),(-2,1), (-1,-2),(-1,2), (1,-2),(1,2), (2,-1),(2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
            

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1,-1),(-1,1),(1,-1),(1,1))#diagonale superiore sinistra, diagonale superiore destra, diagonale inferiore sinistra, diagonale inferiore destra,
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[0]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1), (0,-1), (0,1), (1,-1),(1,0),(1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r+kingMoves[i][0]
            endCol = c+kingMoves[i][1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    in_Check, pins, checks = self.checkForPinsAndChecks()
                    if not in_Check:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # place king back on original location
                    if allyColor == "w":
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        #self.getCastleMoves(r,c,moves)
                        
    #generare tutti gli arrocchi validi per i re a (r,c) e aggiungerli alla lista delle mosse
    def getCastleMoves(self,r,c,moves):
        if self.squareUnderAttack(r,c):
            return #non puoi arroccare per c'è scacco
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastelMoves(r,c,moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastelMoves(r,c,moves)


    def getKingsideCastelMoves(self,r,c,moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c),(r,c+2), self.board, isCastleMove=True))

    
    def getQueensideCastelMoves(self,r,c,moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r,c),(r,c-2), self.board, isCastleMove=True))

   
    

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks #arroco corto
        self.bks = bks
        self.wqs = wqs #arroco lungo
        self.bqs = bqs

class Move():

    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()} 

    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7} 
    colsToFiles = {v: k for k,v in filesToCols.items()} #colsToFiles = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}

    def __init__(self, startSq, endSq, board, isEnPassantMove=False, isCastleMove=False) :
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)
        self.isEnPassantMove= isEnPassantMove#(self.pieceMoved[1] == 'p' and (self.endRow, self.endCol) == enPassantPossible)
        self.isCastleMove = isCastleMove

        if self.isEnPassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.isCapture = self.pieceCaptured != "--"
        #arrocco move

        # if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
        #     self.isPawnPromotion = True
        
        
        # if self.pieceMoved[1] == 'p' and (self.endRow, self.endCol) == enPassantPossible:
        #     self.isEnPassantMove= True
        
        self.moveID = self.startCol * 1000 + self.startRow * 100 + self.endCol * 10 + self.endRow
        # print(self.moveID)


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __str__(self):
        #arrocco
        if self.isCastleMove:
            if self.endCol == 6:
                return "O-O"
            else:
                return "O-O-O"
        endSquare = self.getRankFile(self.endRow, self.endCol)
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare