import pygame as p
import Engine, SMF
from multiprocessing import Process, Queue

questogiocoèunoschifodimerdaporcoilcazzodigabrielecassinatiVENTTTTOTTOSOLFEGGIOEJOHNPORKBATTERISTAJAZZ = True

BOARD_WIDTH = BOARD_HEIGHT = 512 #dimensione finestra
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8 #dimensione della scacchiera
SQ_SIZE = BOARD_HEIGHT // DIMENSION #dimensione quadrato
MAX_FPS = 15 #fps massimi per le animazioni
IMG = {} #dizionario

def load_images():
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wp", "bR", "bN", "bB", "bQ", "bK", "bp"]

    for piece in pieces:       
        IMG[piece] = p.transform.scale(p.image.load("img\\" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) #immagini in scala 512/8
        
#il def main gestirà tutto il codice
def main():
    p.init()
    p.display.set_caption('Chesstnut')
    Icon = p.image.load("img\\logo.jpg")
    p.display.set_icon(Icon)
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("#3E3E3E"))
    r=True
    c=""
    moveLogFont = p.font.SysFont("Arial", 14, False, False)
    gs = Engine.GameState() #gs sta per GameState
    validMoves = gs.getValidMoves()
    moveMade = False #flag che verifica quando avviene una mossa
    animate = False #flag per ogni volta che noi dovremmo "animare" una mossa
    load_images()
    running =True
    sqSelected = () #nessun quadrato selezionato, tiene traccia dell'ultimo click (tuple: (row,col))
    playerClick=[] #tiene traccia dei click del giocatore (List)
    gameOver = False
    playerOne = True #Se il giocatore gioca il bianco
    playerTwo = False #nero
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False
    while r:
        drawBoard(screen)
        for ev in p.event.get(): 
          
            if ev.type == p.QUIT: 
                p.quit() 
                
            
            elif ev.type == p.KEYDOWN:
                if ev.key == p.K_w:
                    playerOne = True
                    playerTwo = False
                    r=False
                    running = True
                    c="white"
                    break

                elif ev.key == p.K_b:
                    playerOne = False 
                    playerTwo = True
                    r=False
                    running = True
                    c="black"
                    break
            else:
                font = p.font.SysFont("Arial", 54, True, False)
                text_object = font.render("Chesstnut", False, p.Color("black"))
                text_location = p.Rect(275,100,BOARD_WIDTH,BOARD_HEIGHT)

                font2 = p.font.SysFont("Arial", 24, True, False)
                text_object2 = font2.render("Press 'W' to play white, if press 'B' to play black", False, p.Color("black"))
                text_location2 = p.Rect(190,220,BOARD_WIDTH,BOARD_HEIGHT)

                screen.blit(text_object, text_location)
                screen.blit(text_object2, text_location2)
                p.display.update()


    while running:
        HumanTrun = (gs.whiteToMove and playerOne)or(not gs.whiteToMove and playerTwo)
        if HumanTrun:
            fontp = p.font.SysFont("Arial", 30, True, False)
            point_object = fontp.render("Y", False, p.Color(c))
            point_location = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH+5, MOVE_LOG_PANEL_HEIGHT)
            screen.blit(point_object, point_location)
        p.display.update()
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col) or col >= 8: #l'utente clicca due volte lo stesso quadrato
                        sqSelected=()#deselezionato
                        playerClick = []
                    else:
                        sqSelected= (row, col)
                        playerClick.append(sqSelected) #aggiunge il primo e il secondo click
                    if len(playerClick)==2 and HumanTrun:
                        move = Engine.Move(playerClick[0], playerClick[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected=()
                                playerClick=[]
                        if not moveMade:
                            playerClick = [sqSelected]


            elif e.type == p.KEYDOWN:
                if e.key == p.K_LEFT:
                    gs.undoMove()
                    sqSelected = ()
                    playerClick = []
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True
                if e.key == p.K_r: #resetta la partita/scacchiera quando premi 'r'
                    gs = Engine.GameState() #gs sta per GameState
                    validMoves = gs.getValidMoves()
                    # moveMade = False #flag che verifica quando avviene una mossa
                    # animate = False #flag per ogni volta che noi dovremmo "animare" una mossa
                    # running =True
                    sqSelected = () #nessun quadrato selezionato, tiene traccia dell'ultimo click (tuple: (row,col))
                    playerClick=[] #tiene traccia dei click del giocatore (List)
                    moveMade = False
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True



        if not gameOver and not HumanTrun and not moveUndone:
            if not AIThinking:
                AIThinking = True
                print("thinking...")
                returnQueue = Queue() #used to pass between threads
                moveFinderProcess = Process(target=SMF.findBestMove, args=(gs, validMoves, returnQueue))
                moveFinderProcess.start() #richiama findBestMove
                
            if not moveFinderProcess.is_alive():
                print("done")
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = SMF.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                moveMade = True
                animate = True
                AIThinking = False


        if moveMade:
            if animate:
                animationMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves= gs.getValidMoves()
            moveMade=False
            animate=False
            moveUndone = False


        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkmate or gs.stalemate:
            gameOver=True
            if gs.stalemate:
                drawEndGameText(screen, "1/2-1/2 Draw by stalemate")
            else:
                drawEndGameText(screen, "Black wins by checkmate 0-1") if gs.whiteToMove else drawEndGameText(screen, "White wins by checkmate 1-0")
                # text
                # if gs.whiteToMove:
                #     text='0-1 Black wins by checkmate'
                # else:
                #     text='1-0 White wins by checkmate'

        clock.tick(MAX_FPS)
        p.display.flip()


#evidenzia il quadrato selezionato e muovere il pezzo
def highlightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r,c=sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected è un pezzo che può esser mosso
            #evidenziare il quadrato selezionato
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100) #trasparenza da 0 a 255
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            #evidenza le mosse da quel quadrato
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))


def drawGameState(screen, gs, validMoves, sqSelected,moveLogFont):
    drawBoard(screen)
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)

def drawBoard(screen):
    global colors
    colors=[p.Color("#f9dbbe"), p.Color("#C29467")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMG[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("#3E3E3E"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveStr = str(i//2 +1) + ". " + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveStr += str(moveLog[i+1])+"   "
        moveTexts.append(moveStr)

    movesPerRow = 3
    padding = 30
    textY = 5
    lineSpecing = 2
    for i in range(0,len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        
        if gs.checkmate:
            if not gs.whiteToMove:
                text += " 1-0"
            else:
                text += " 0-1"
        elif gs.stalemate:
            text += " 1/2-1/2"

        textObject = font.render(text,True,p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpecing

#animazione del pezzo
def animationMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framePerSquare = 10 #frame per muoversi in un quadrato
    frameCount = (abs(dR)+abs(dC)) * framePerSquare
    for frame in range(frameCount+1):
        r,c=(move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #disegna il pezzo catturato sul rettangolo
        if move.pieceCaptured != '--':
            if move.isEnPassantMove:
                enPassantRow = move.endRow+1 if move.pieceCaptured[0] == 'b' else move.endRow-1
                endSquare = p.Rect(move.endCol*SQ_SIZE, enPassantRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
            screen.blit(IMG[move.pieceCaptured], endSquare)
        #disegna il movimento
        if move.pieceMoved !='--':
            screen.blit(IMG[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawEndGameText(screen, text):
    # font = p.font.SysFont("Helvitca", 32, True, False)
    # textObject = font.render(text,0,p.Color('Black'))
    # textLocation = p.Rect(0,0,BOARD_WIDTH,BOARD_HEIGHT).move(BOARD_WIDTH/2 -textObject.get_width()/2, BOARD_HEIGHT/2 -textObject.get_height()/2)
    # screen.blit(textObject, textLocation)
    font = p.font.SysFont("Arial", 32, True, False)
    text_object = font.render(text, False, p.Color("lightgray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))

if __name__ == "__main__":
    main()