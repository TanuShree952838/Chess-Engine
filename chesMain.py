#GUI controller
import pygame as p
import sys
from chess import ChessEngine
import pygame.gfxdraw

WIDTH = 936
HEIGHT = 663
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION-24
MAX_FPS = 15 #FOR ANIMATION EFFECTS
IMAGES = {}
KILLS = {}
HOME = True

#INITIALIZE GLOBAL DICTIONARY OF IMAGES WHICH CALLED ONLY ONCE

def loadImages():
    pieces = ['wp','wR', 'wN', 'wB', 'wK', 'wQ','bp','bR', 'bN', 'bB', 'bK', 'bQ' ]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))
        KILLS[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (47, 47))


# home Page
def home():
    p.init()
    print(SQ_SIZE)
    screen = p.display.set_mode((WIDTH, HEIGHT))
    iconImage= p.image.load("images/icon.png")
    p.display.set_icon(iconImage)
    p.display.set_caption("CHESS CLUB")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    screen.blit(p.transform.scale(p.image.load("images/HP.png"), (WIDTH, HEIGHT)),
                p.Rect(0, 0, WIDTH, HEIGHT))


    hrunning = True

    while hrunning:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                p.quit()
                sys.exit()
                hrunning = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                if 231 < location[0] < 903 and 416 < location[1] < 474:
                    withAI(screen, clock)
                    hrunning = False
                    main(True)

                elif 176 < location[0] < 811 and 309 < location[1] < 346:
                    withFriends(screen, clock)
                    hrunning = False
                    main(False)

                elif 728 < location[0] < 926 and 582 < location[1] < 615:
                    Quit(screen, clock)
                    p.quit()
                    sys.exit()
                    hrunning = False
        clock.tick(MAX_FPS)
        p.display.flip()
#Home Page buttons
def Quit(screen,clock):
    react = p.Rect(0, 0, 926 - 712, 615 - 558)
    s = p.Surface((926 - 712, 615 - 558))
    s.set_alpha(100)
    s.fill(p.Color("#E69271"))
    draw_rounded_rect(s, react, p.Color("red"), 10)
    screen.blit(s, (720, 572))
    for f in range(10):
        screen.blit(p.transform.scale(p.image.load("images/HP.png"), (WIDTH, HEIGHT)),
                    p.Rect(0, 0, WIDTH, HEIGHT))
        screen.blit(s, (720, 572))
        p.display.flip()
        clock.tick(60)
def withAI(screen,clock):
    react = p.Rect(0, 0, 811 - 100, 346 - 270)
    s = p.Surface((811 - 100, 346 - 270))
    s.set_alpha(100)
    s.fill(p.Color("#E69271"))
    draw_rounded_rect(s, react, p.Color("red"), 10)
    screen.blit(s, (200, 410))
    for f in range(10):
        screen.blit(p.transform.scale(p.image.load("images/HP.png"), (WIDTH, HEIGHT)),
                    p.Rect(0, 0, WIDTH, HEIGHT))
        screen.blit(s, (200, 410))
        p.display.flip()
        clock.tick(60)

def withFriends(screen,clock):
    react = p.Rect(0, 0, 811 - 145, 346 - 270)
    s = p.Surface((811 - 145, 346 - 270))
    s.set_alpha(100)
    s.fill(p.Color("#E69271"))
    draw_rounded_rect(s, react, p.Color("red"), 10)
    screen.blit(s, (150, 292))
    for f in range(10):
        screen.blit(p.transform.scale(p.image.load("images/HP.png"), (WIDTH, HEIGHT)),
                    p.Rect(0, 0, WIDTH, HEIGHT))
        screen.blit(s, (150, 290))
        p.display.flip()
        clock.tick(60)






#the main driver for the code whch will handle the user input and updating graphics.

def main(AI):
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    iconImage = p.image.load("images/icon.png")
    p.display.set_icon(iconImage)
    p.display.set_caption("CHESS CLUB")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    #screen.blit(p.transform.scale(p.image.load("images/CB.png"),(WIDTH+40,HEIGHT)), p.Rect(0, 0, WIDTH+40, HEIGHT))
    gs = ChessEngine.GameState(AI)
    validMoves = gs.getValidMoves()
    movemade = False
    animate = False
    undo = False
    restart = False
    homeC = False
    gameOver = False
    pawnP = False
    promo = None
    loadImages()
    running=True
    sqSelected = ()          #no square selected.
    playerClicks = []#keep track of player clicks.
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
            if (gs.whiteToMove) or (not gs.AI):
                if e.type == p.MOUSEBUTTONDOWN:
                    if not gameOver:
                        location = p.mouse.get_pos() #(x,y) coordinates
                        if 30 <= location[0] <= 494 and 156 <= location[1] <= 620:
                            col = (location[0] - 30)//SQ_SIZE
                            row = (location[1]- 156)//SQ_SIZE
                            if sqSelected == (row, col):
                                sqSelected = ()
                                playerClicks = []
                            else:
                                sqSelected = (row, col)
                                playerClicks.append(sqSelected)   #apend for both first and second click

                            if len(playerClicks) == 2 : #after 2 click
                                move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)

                                for i in range(len(validMoves)):
                                    if move == validMoves[i]:
                                        if (move.pieceMoved == "wp" and move.endRow == 0) or (
                                                move.pieceMoved == "bp" and move.endRow == 7) and not gs.AI:
                                            pawnP = True
                                            promo = validMoves[i]
                                        else:
                                            gs.makeMove(validMoves[i])
                                            movemade=True
                                            animate = True
                                            sqSelected = ()
                                            playerClicks = []
                                    if not movemade:
                                        playerClicks = [sqSelected]
                        elif 562 <= location[0] <= 728 and 507 <= location[1] <= 590:
                            drawRestart(screen, gs, validMoves, sqSelected, clock)
                            gs = ChessEngine.GameState(AI)
                            validMoves = gs.getValidMoves()
                            sqSelected = ()
                            playerClicks = []
                            movemade = False
                            animate = False
                            gameOver = False

                        elif 750 <= location[0] <= 920 and 512 <= location[1] <= 588:
                            drawUndo(screen, gs, validMoves, sqSelected, clock)
                            gs.undoMove()
                            if gs.AI:
                                gs.undoMove()
                            movemade = True
                            animate = False
                            gameOver = False
                        elif 7 < location[1] < 129 and 12 < location[1] < 46:
                            drawHome(screen, gs, validMoves, sqSelected, clock)
                            running = False
                            home()
            else:
                if not gameOver:
                    p.display.set_caption("Calculating move...")
                    mov = gs.minimaxRoot(3, True)
                    gs.makeMove(mov)
                    p.display.set_caption("CHESS CLUB")
                    print("ndjk")
                    print(gs.lastMove[-2])
                    print(gs.lastMove[-1])
                    movemade = True
                    animate = True
                    sqSelected = ()
                    playerClicks = []
                    gs.whiteToMove = True
                    print("black move...")
                    validMoves = gs.getValidMoves()

                    '''sqSelected = (1, 1)
                    playerClicks.append(sqSelected)#apend for both first and second click
                    sqSelected = (3,1)
                    playerClicks.append(sqSelected)  # apend for both first and second click
                    print(playerClicks)

                    if len(playerClicks) == 2 : #after 2 click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)

                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                print("fkh")
                                gs.makeMove(validMoves[i])
                                movemade=True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                    gs.whiteToMove = True
                    print("black move...")
                    validMoves = gs.getValidMoves()'''

            if gameOver:
                if e.type == p.MOUSEBUTTONDOWN :
                    location = p.mouse.get_pos()  # (x,y) coordinates
                    if 473 < location[0] < 553 and 390 < location[1] < 405:
                        react = p.Rect(0, 0, 553 - 457, 405 - 372)
                        s = p.Surface((553 - 457, 405 - 372))
                        s.set_alpha(100)
                        s.fill(p.Color("#E69271"))
                        draw_rounded_rect(s, react, p.Color("red"), 5)
                        screen.blit(s, (470, 390))
                        for f in range(10):
                            if gs.stalemate:
                                drawText(screen, 'SM')
                            elif gs.whiteToMove:
                                drawText(screen, 'BW')
                            else:
                                drawText(screen, 'WW')
                            screen.blit(s, (468, 386))
                            p.display.flip()
                            clock.tick(60)
                        gs.undoMove()
                        if gs.AI:
                            gs.undoMove()
                        movemade = True
                        animate = False
                        gameOver = False
                    elif 258 < location[0] < 373 and 385 < location[1] < 405:
                        react = p.Rect(0, 0, 553 - 410, 405 - 365)
                        s = p.Surface((553 - 410, 405 - 365))
                        s.set_alpha(100)
                        s.fill(p.Color("#E69271"))
                        draw_rounded_rect(s, react, p.Color("red"), 5)
                        screen.blit(s, (245, 380))
                        for f in range(10):
                            if gs.stalemate:
                                drawText(screen, 'SM')
                            elif gs.whiteToMove:
                                drawText(screen, 'BW')
                            else:
                                drawText(screen, 'WW')
                            screen.blit(s, (245, 380))
                            p.display.flip()
                            clock.tick(60)
                        gs = ChessEngine.GameState(AI)
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        movemade = False
                        animate = False
                        gameOver = False
                    elif 154 < location[0] < 269 and 177 < location[1] < 203 :
                        react = p.Rect(0, 0, 553 - 410, 405 - 360)
                        s = p.Surface((553 - 410, 405 - 360))
                        s.set_alpha(100)
                        s.fill(p.Color("#E69271"))
                        draw_rounded_rect(s, react, p.Color("red"), 5)
                        screen.blit(s, (157, 177))
                        for f in range(10):
                            if gs.stalemate:
                                drawText(screen, 'SM')
                            elif gs.whiteToMove:
                                drawText(screen, 'BW')
                            else:
                                drawText(screen, 'WW')
                            screen.blit(s, (138, 168))
                            p.display.flip()
                            clock.tick(60)
                        running = False
                        home()


            if pawnP and not gameOver:
                if e.type == p.MOUSEBUTTONDOWN :
                    location = p.mouse.get_pos()
                    print(location)
                    if 250< location[0] < 308 and 305 < location[1] < 365:
                        print(location)
                        s = p.Surface((308 - 240, 365- 295))
                        s.set_alpha(100)
                        s.fill(p.Color("red"))
                        #draw_rounded_rect(s, react, p.Color("red"), 5)
                        screen.blit(s, (250, 305))
                        for f in range(10):
                            if gs.whiteToMove:
                                drawPromotion(screen, 'WP')
                            else:
                                drawPromotion(screen, 'BP')
                            screen.blit(s, (245, 300))
                            p.display.flip()
                            clock.tick(60)
                        gs.chosepiece = 'B'
                        gs.makeMove(promo)
                        movemade = True
                        animate = True
                        sqSelected = ()
                        playerClicks = []
                        pawnP = False
                        gs.pawnPromotion = False
                    elif 340 < location[0] < 398 and 305 < location[1] < 365:
                        print(location)

                        s = p.Surface((308 - 240, 365 - 295))
                        s.set_alpha(100)
                        s.fill(p.Color("red"))
                        # draw_rounded_rect(s, react, p.Color("red"), 5)
                        screen.blit(s, (335, 305))
                        for f in range(10):
                            if gs.whiteToMove:
                                drawPromotion(screen, 'WP')
                            else:
                                drawPromotion(screen, 'BP')
                            screen.blit(s, (335, 300))
                            p.display.flip()
                            clock.tick(60)

                        gs.chosepiece = 'R'
                        gs.makeMove(promo)
                        movemade = True
                        animate = True
                        sqSelected = ()
                        playerClicks = []
                        pawnP = False
                        gs.pawnPromotion = False
                    elif 422< location[0] < 481 and 305 < location[1] < 365:
                        print(location)
                        s = p.Surface((308 - 240, 365 - 295))
                        s.set_alpha(100)
                        s.fill(p.Color("red"))
                        # draw_rounded_rect(s, react, p.Color("red"), 5)
                        screen.blit(s, (422, 305))
                        for f in range(10):
                            if gs.whiteToMove:
                                drawPromotion(screen, 'WP')
                            else:
                                drawPromotion(screen, 'BP')
                            screen.blit(s, (419, 305))
                            p.display.flip()
                            clock.tick(60)

                        gs.chosepiece = 'N'
                        gs.makeMove(promo)
                        movemade = True
                        animate = True
                        sqSelected = ()
                        playerClicks = []
                        pawnP = False
                        gs.pawnPromotion = False
                    elif 506< location[0] < 566 and 305 < location[1] < 365:
                        print(location)

                        s = p.Surface((308 - 240, 365 - 295))
                        s.set_alpha(100)
                        s.fill(p.Color("red"))
                        # draw_rounded_rect(s, react, p.Color("red"), 5)
                        screen.blit(s, (502, 305))
                        for f in range(10):
                            if gs.whiteToMove:
                                drawPromotion(screen, 'WP')
                            else:
                                drawPromotion(screen, 'BP')
                            screen.blit(s, (502, 305))
                            p.display.flip()
                            clock.tick(60)

                        gs.chosepiece = 'Q'
                        gs.makeMove(promo)
                        movemade = True
                        animate = True
                        sqSelected = ()
                        playerClicks = []
                        pawnP = False
                        gs.pawnPromotion = False
                    if 565 < location[0] < 642 and 403 < location[1] < 441:
                        print("hdfg")
                        react = p.Rect(0, 0, 642 - 555 , 441 - 400)
                        s = p.Surface((642 - 555, 441 - 400))
                        s.set_alpha(100)
                        s.fill(p.Color("#E69271"))
                        draw_rounded_rect(s, react, p.Color("red"), 10)
                        screen.blit(s, (560, 390))
                        for f in range(10):
                            if gs.whiteToMove:
                                drawPromotion(screen, 'WP')
                            else:
                                drawPromotion(screen, 'BP')
                            screen.blit(s, (562, 390))
                            p.display.flip()
                            clock.tick(60)

                        gs.chosepiece = 'N'
                        gs.makeMove(promo)
                        gs.undoMove()
                        movemade = True
                        animate = False
                        sqSelected = ()
                        playerClicks = []
                        pawnP = False
                    elif 154 < location[0] < 269 and 177 < location[1] < 203 :
                        print(location)

                        react = p.Rect(0, 0, 642 - 515, 441 - 390)
                        s = p.Surface((642 - 515, 441 - 390))
                        s.set_alpha(100)
                        s.fill(p.Color("#E69271"))
                        draw_rounded_rect(s, react, p.Color("red"), 10)
                        screen.blit(s, (145, 167))
                        for f in range(10):
                            if gs.whiteToMove:
                                drawPromotion(screen, 'WP')
                            else:
                                drawPromotion(screen, 'BP')
                            screen.blit(s, (145, 167))
                            p.display.flip()
                            clock.tick(60)

                        running = False
                        home()

                if e.type == p.KEYDOWN:
                    if e.key == p.K_z:
                        print("hdfg")
                        gs.chosepiece = 'N'
                        gs.makeMove(promo)
                        gs.undoMove()
                        movemade = True
                        animate = False
                        sqSelected = ()
                        playerClicks = []
                        pawnP = False
                    if e.key == p.K_r:
                        gs = ChessEngine.GameState(AI)
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        pawnP = False
                        movemade = False
                        animate = False
                        gameOver = False


        if movemade:
            if animate and not pawnP:
                animateMove(gs.movelog[-1], screen, gs.board, clock)
            validMoves=gs.getValidMoves()
            movemade = False
            animate = False
        if not pawnP:
            drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'BW')
            else:
                drawText(screen, 'WW')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'SM')
        elif pawnP:
            if gs.whiteToMove:
                drawPromotion(screen, 'WP')
            else:
                drawPromotion(screen, 'BP')

        clock.tick(MAX_FPS)
        p.display.flip()


#HighLight square selected and the move of the selected piece
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        #Heighlight Selected square
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('green'))
            screen.blit(s, (c*SQ_SIZE + 30, r*SQ_SIZE + 156))

            # highlight th moves of the selected piece
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE + 30 , move.endRow*SQ_SIZE + 156))
#draw Restart
def drawRestart(screen,gs,validMoves,sqSelected, clock):
    react = p.Rect(0, 0, 728 - 556, 590 - 505)
    s = p.Surface((728 - 556, 590 - 505))
    s.set_alpha(100)
    s.fill(p.Color("#E69271"))
    draw_rounded_rect(s, react, p.Color("red"), 30)
    screen.blit(s, (556, 504))
    for f in range(10):
        drawGameState(screen, gs, validMoves, sqSelected)
        screen.blit(s, (556, 504))
        p.display.flip()
        clock.tick(60)
#drw home
def drawHome(screen,gs,validMoves,sqSelected, clock):
    react = p.Rect(0, 0, 132, 48)
    s = p.Surface((132, 48))
    s.set_alpha(100)
    s.fill(p.Color("#E69271"))
    draw_rounded_rect(s, react, p.Color("red"), 15)
    screen.blit(s, (3, 6))
    for f in range(10):
        drawGameState(screen, gs, validMoves, sqSelected)
        screen.blit(s, (3, 6))
        p.display.flip()
        clock.tick(60)
#draw Undo
def drawUndo(screen,gs,validMoves,sqSelected, clock):
    react = p.Rect(0, 0, 920 - 750, 588 - 505)
    s = p.Surface((920 - 750, 588 - 500))
    s.set_alpha(100)
    s.fill(p.Color("#E69271"))
    draw_rounded_rect(s, react, p.Color("red"), 30)
    screen.blit(s, (742, 505))
    for f in range(10):
        drawGameState(screen, gs, validMoves, sqSelected)
        screen.blit(s, (742, 505))
        p.display.flip()
        clock.tick(60)
def draw_rounded_rect(surface, rect, color, corner_radius):
    ''' Draw a rectangle with rounded corners.
    Would prefer this:
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    but this option is not yet supported in my version of pygame so do it ourselves.

    We use anti-aliased circles to make the corners smoother
    '''
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    p.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    p.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    p.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    p.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    p.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    p.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    p.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    p.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    rect_tmp = p.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    p.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    p.draw.rect(surface, color, rect_tmp)
#draw last move
def highlightLastMove(screen, gs):
    if gs.lastMove != []:
        Er = gs.lastMove.pop()
        Ec = gs.lastMove.pop()
        Sr = gs.lastMove.pop()
        Sc = gs.lastMove.pop()
        gs.lastMove = []
        gs.lastMove.append(Sc)
        gs.lastMove.append(Sr)
        gs.lastMove.append(Ec)
        gs.lastMove.append(Er)
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('blue'))
        screen.blit(s, (Ec * SQ_SIZE + 30, Er * SQ_SIZE + 156))
        screen.blit(s, (Sc * SQ_SIZE + 30, Sr * SQ_SIZE + 156))

# draw all graphics for current state
def drawGameState(screen,gs, validMoves, sqSelected):
    screen.blit(p.transform.scale(p.image.load("images/CB.png"), (WIDTH, HEIGHT)),
                p.Rect(0, 0, WIDTH, HEIGHT))
    drawBoard(screen)#draw squares on the boasrd
    drawPlayer1(screen, gs.player2)
    drawPlayer2(screen, gs.player1)
    highlightLastMove(screen, gs, )
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)




def drawBoard(screen):
    global colors
    colors = [p.Color('#FACB9D'), p.Color("#CD8842")]
    colo = p.Color("black")
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(30+c*SQ_SIZE, 156+r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.draw.rect(screen, colo, p.Rect(30, 152,58*8, 3))
    p.draw.rect(screen, colo, p.Rect(27, 152, 3,58 * 8 +7))
    p.draw.rect(screen, colo, p.Rect(493, 152, 3, 58 * 8+7))
    p.draw.rect(screen, colo, p.Rect(30, 620, 58 * 8, 3))

def drawPlayer1(screen, board):
    box = 47
    for r in range(2):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":# Check for empityness.
                screen.blit(KILLS[piece], p.Rect(511+c*box,226 + r*box, box, box))

def drawPlayer2(screen, board):
    box = 47
    for r in range(2):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":# Check for empityness.
                screen.blit(KILLS[piece], p.Rect(511+c*box,382+ r*box, box, box))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":# Check for empityness.
                screen.blit(IMAGES[piece], p.Rect(30+c*SQ_SIZE,156+ r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Animating moves..
def animateMove(move, screen, board, clock):
    global colors
    coords = [] #list of coordinates
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE + 30, move.endRow*SQ_SIZE + 156, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured Piece
        if move.piececaptured != '--':
            screen.blit(IMAGES[move.piececaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE + 30, r*SQ_SIZE +156, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
def drawPromotion(screen, text):
    if text == 'WP':
        img = p.transform.scale(p.image.load("images/Wprom.png"), (536, 272))
        screen.blit(img, p.Rect(WIDTH / 2 - 334, HEIGHT / 2 - 170, 536, 272))
    elif text == 'BP':
        img = p.transform.scale(p.image.load("images/Bprom.png"), (536, 272))
        screen.blit(img, p.Rect(WIDTH / 2 - 334, HEIGHT / 2 - 170, 536, 272))


def drawText(screen, text):
    if text == 'WW':
        img = p.transform.scale(p.image.load("images/WW.png"),(536,272))
        screen.blit(img, p.Rect(WIDTH/2 - 334, HEIGHT/2 - 170, 536, 272))
    elif text == 'BW':
        img = p.transform.scale(p.image.load("images/BW.png"), (536, 272))
        screen.blit(img, p.Rect(WIDTH / 2 - 334, HEIGHT / 2 - 170, 536, 272))
    elif text == 'SM':
        img = p.transform.scale(p.image.load("images/SM.png"), (536, 272))
        screen.blit(img, p.Rect(WIDTH / 2 - 334, HEIGHT / 2 - 170, 536, 272))


