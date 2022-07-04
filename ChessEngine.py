#moves controlling
from  chess import  chesMain
import random

class GameState():
    def __init__(self, AI):
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.player1 = [["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"]]
        self.player2 = [["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"]]
        self.play1 = 0
        self.play2 = 0

        #AI bonus calc
        self.ROOK_SEMI_OPEN_FILE_BONUS = 10
        self.ROOK_ON_SEVENTH_BONUS = 20
        self.PAWN_BONUS = [0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, -40, -40, 0, 0, 0,
                      1, 2, 3, -10, -10, 3, 2, 1,
                      2, 4, 6, 8, 8, 6, 4, 2,
                      3, 6, 9, 12, 12, 9, 6, 3,
                      4, 8, 12, 16, 16, 12, 8, 4,
                      5, 10, 15, 20, 20, 15, 10, 5,
                      0, 0, 0, 0, 0, 0, 0, 0]

        self.KNIGHT_BONUS = [-10, -30, -10, -10, -10, -10, -30, -10,
                        -10, 0, 0, 0, 0, 0, 0, -10,
                        -10, 0, 5, 5, 5, 5, 0, -10,
                        -10, 0, 5, 10, 10, 5, 0, -10,
                        -10, 0, 5, 10, 10, 5, 0, -10,
                        -10, 0, 5, 5, 5, 5, 0, -10,
                        -10, 0, 0, 0, 0, 0, 0, -10,
                        -10, -10, -10, -10, -10, -10, -10, -10]

        self.BISHOP_BONUS = [-10, -10, -20, -10, -10, -20, -10, -10,
                        -10, 0, 0, 0, 0, 0, 0, -10,
                        -10, 0, 5, 5, 5, 5, 0, -10,
                        -10, 0, 5, 10, 10, 5, 0, -10,
                        -10, 0, 5, 10, 10, 5, 0, -10,
                        -10, 0, 5, 5, 5, 5, 0, -10,
                        -10, 0, 0, 0, 0, 0, 0, -10,
                        -10, -10, -10, -10, -10, -10, -10, -10]

        self.KING_BONUS = [0, 20, 40, -20, 0, -20, 40, 20,
                      -20, -20, -20, -20, -20, -20, -20, -20,
                      -40, -40, -40, -40, -40, -40, -40, -40,
                      -40, -40, -40, -40, -40, -40, -40, -40,
                      -40, -40, -40, -40, -40, -40, -40, -40,
                      -40, -40, -40, -40, -40, -40, -40, -40,
                      -40, -40, -40, -40, -40, -40, -40, -40,
                      -40, -40, -40, -40, -40, -40, -40, -40]

        self.KING_ENDGAME_BONUS = [0, 10, 20, 30, 30, 20, 10, 0,
                              10, 20, 30, 40, 40, 30, 20, 10,
                              20, 30, 40, 50, 50, 40, 30, 20,
                              30, 40, 50, 60, 60, 50, 40, 30,
                              30, 40, 50, 60, 60, 50, 40, 30,
                              20, 30, 40, 50, 50, 40, 30, 20,
                              10, 20, 30, 40, 40, 30, 20, 10,
                              0, 10, 20, 30, 30, 20, 10, 0]





        self.whiteToMove = True
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getknightMoves, 'B': self.getBisopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}
        self.movelog = []
        self.lastMove = [] #track last move
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.incheck = False
        self.pins = []
        self.checks = ()
        self.checkmate = False
        self.pawnPromotion = False
        self.AI = AI
        self.chosepiece = 'Q'
        self.stalemate = False #when the king is not in check but still dont have any valid maoves
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        self.empassantPossible = () #coordinates of the squre on which emphassant  is possible

    def flip(self):
        board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        for i in range(8):
            for j in range(8):
                board[i][j] = self.board[7-i][7-j]
        return board


    def makeMove(self, move):
        self.flip()
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        #pawn promotion
        self.pawnPromotion = move.ispawnPromotion
        if move.ispawnPromotion:
            #while(self.pawnPromotion):
                #print("d")
            if self.AI:
                chosePiece = 'Q'
            else:
                chosePiece = 'N'
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + self.chosepiece
        pieceDrawn= False

        self.lastMove.append(move.startCol)
        self.lastMove.append(move.startRow)
        self.lastMove.append(move.endCol)
        self.lastMove.append(move.endRow)
        if move.piececaptured != '--':
            for i in range(2):
                if not pieceDrawn:
                    for j in range(8):
                        if self.whiteToMove:
                            if self.player1[i][j] == '--':
                                self.player1[i][j] = move.piececaptured
                                self.play1 = self.play1 + 1
                                print(self.play1)
                                pieceDrawn = True
                                break
                        else:
                            if self.player2[i][j] == '--':
                                self.player2[i][j] = move.piececaptured
                                self.play2 = self.play2 + 1
                                print(self.play2)
                                pieceDrawn = True
                                break

        self.whiteToMove = not self.whiteToMove #switch the players.
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)

        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        #Castle move
        if move.iscastleMove:
            if move.endCol - move.startCol == 2: #King side castling
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol+1] = '--'

            else: #Queen side castlng
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol -2]
                self.board[move.endRow][move.endCol -2] = '--'


        # update castlingRights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

        '''# Pawn empassant
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.empassantPossible = ((move.endRow + move.startRow)//2 , move.endCol)
        else:
            self.empassantPossible = ()
        if move.enPassant:
            self.board[move.startRow][move.startCol] = "--"

        #Pawn promotion
        if move.pawnPromotion:
            promotedPiece = input("Promote to Q, R, B, or N :")
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece'''

    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol]=move.piececaptured
            if len(self.movelog) != 0:
                self.lastMove.append(self.movelog[-1].startCol)
                self.lastMove.append(self.movelog[-1].startRow)
                self.lastMove.append(self.movelog[-1].endCol)
                self.lastMove.append(self.movelog[-1].endRow)
            else:
                self.lastMove = []
            self.pawnPromotion = False
            if move.piececaptured != '--':
                if self.whiteToMove:
                    self.play2 = self.play2 - 1
                    if self.play2 < 8:
                        self.player2[0][self.play2] = '--'
                    else:
                        self.player2[1][self.play2 - 8] = '--'
                    print("pay2", self.play2)

                else:
                    self.play1 = self.play1 - 1
                    print(self.play1)
                    if self.play1 < 8:
                        self.player1[0][self.play1] = '--'
                    else:
                        self.player1[1][self.play1 - 8] = '--'



            '''if move.piececaptured != '--':
                piecePop = False
                for i in reversed(range(2)):
                    if not piecePop:
                        for j in reversed(range(8)):
                            if self.whiteToMove:
                                if self.player1[i][j] != '--':
                                    self.player1[i][j] = '--'
                                    piecePop = True
                                    break
                            else:
                                if self.player2[i][j] != '--':
                                    self.player2[i][j] = '--'
                                    piecePop = True
                                    break'''


            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)

            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo castle rights
            self.castleRightsLog.pop()
            castleRight = self.castleRightsLog[-1]
            self.currentCastlingRight = castleRight
            # UNDO CASTLE MOVE
            if move.iscastleMove:
                if move.endCol - move.startCol == 2 :
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol-1] ='--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
            ''''#undo emphassant
            if move.enPassant:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] == move.piececaptured
                self.empassantPossible = (move.endRow, move.endCol)

            #undo a 2 square pawn advance should make emphassantPossible =()
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.empassantPossible = ()'''

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

    #All moves considerig checks
    def getValidMoves(self):
        moves = []
        tempCastling= self.currentCastlingRight


        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != "K":
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastlingMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastlingMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        self.currentCastlingRight= tempCastling

        if len(moves) == 0:  # eithere checkMate or the stalemade...
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves


        '''moves = self.getAllPossibleMoves()

        # 2) For each move make the move
        for i in  range(len(moves)-1, -1, -1  ):
            self.makeMove(moves[i])
            # 3) Generate the opponent moves
            # 4) for each opponent move see if they can attack the king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) # 5) if they can attack your king then its not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves)== 0: #eithere checkMate or the stalemade...
            if self.inCheck():
                self.checkMate=True
            else:
                self.staleMate=True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves'''

#   TO GENERATE AI MOVES......
    def minimaxRoot(self, depth, isMaximizing):
        possibleMoves =self.getValidMoves()
        print(possibleMoves)
        bestMove = -9999
        movlog = []
        bestMoveFinal = None
        for i in possibleMoves:
            move = i
            if move.pieceMoved[0] == 'b':
                self.makeMove(move)
                value = max(bestMove, self.minimax(depth - 1,-10000, 1000, not isMaximizing))
                if value > bestMove:
                    movlog = []
                    movlog.append(move)
                elif value == bestMove:
                    movlog.append(move)
                self.undoMove()
                print("Best score: ", str(bestMove))
                print("Best move: ", str(bestMoveFinal))
                bestMove = value
        bestMoveFinal = random.choice(movlog)
        return bestMoveFinal

    def minimax(self, depth,alpha, beta, is_maximizing):
        if (depth == 0):
            if is_maximizing:
                return self.evaluate_game()
            else:
                return -self.evaluate_game()
        possibleMoves = self.getValidMoves()
        if (is_maximizing):
            bestMove = -9999
            movlog = []
            for i in possibleMoves:
                move = i
                if move.pieceMoved[0] == 'b':
                    self.makeMove(move)
                    value = max(bestMove, self.minimax(depth - 1,alpha, beta, not is_maximizing))
                    self.undoMove()
                    alpha = max(alpha, bestMove)
                    if beta < alpha:
                        return bestMove
            return bestMove
        else:
            bestMove = 9999
            for i in possibleMoves:
                move = i
                if move.pieceMoved[0] == 'w':
                    self.makeMove(move)
                    bestMove = min(bestMove, self.minimax(depth - 1,alpha, beta, not is_maximizing))
                    self.undoMove()
                    beta = min(beta, bestMove)
                    if (beta < alpha):
                        return bestMove
            return bestMove

    def evaluate_game(self):
            return self.evaluation() + self.positional_balance()

    def positional_balance(self):
        return self.positional_bonus("b") - self.positional_bonus("w")
    def evaluation(self):
        eval = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j][0] == 'b':
                    eval = eval + self.getPieceValue(self.board[i][j][1])
                else:
                    eval = eval - self.getPieceValue(self.board[i][j][1])
        return eval

    def positional_bonus(self, color):
        bonus = 0
        if color == "b":
            board = self.board
        elif color =="w":
            board = self.flip()

        for i in range(8):
            for j in range(8):
                piece = board[i][j]

                if piece != "--" and piece[0] == color:
                    print(piece)
                    piece_type = piece[1]

                    if piece_type == "p":
                        bonus += self.PAWN_BONUS[i*8 + j]
                    elif piece_type == "N":
                        bonus += self.KNIGHT_BONUS[i*8 + j]
                    elif piece_type == "B":
                        bonus += self.BISHOP_BONUS[i*8 + j]

                    elif piece_type == "R":
                        if i == 7:
                            bonus += self.ROOK_ON_SEVENTH_BONUS
                        else:
                            bonus += self.ROOK_SEMI_OPEN_FILE_BONUS
                           
                    elif piece_type == "K":
                        bonus += self.KING_BONUS[i*8 + j]
        return bonus


    def getPieceValue(self,piece):
        if (piece == None):
            return 0
        value = 0
        if piece == "P" or piece == "p":
            value = 100
        if piece == "N" or piece == "n":
            value = 300
        if piece == "B" or piece == "b":
            value = 300
        if piece == "R" or piece == "r":
            value = 500
        if piece == "Q" or piece == "q":
            value = 900
        if piece == 'K' or piece == 'k':
            value = 45000
        # value = value if (board.piece_at(place)).color else -value
        return value
    #Determine is the current player in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    #Detertmine if the enimy can attack the square r, c
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # to create opponent moves
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: # square under attack
                return True
        return False

    #All moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enimyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enimyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1),(1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K":
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])

                        else:
                            break
                    elif endPiece[0] == enimyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == "R") or \
                                (4 <= j <= 7 and type == "B") or \
                                (i == 1 and type == "p" and ((enimyColor == "w" and 6 <= j <= 7) or (enimyColor == "b" and 4 <= j <= 5))) or \
                                (type == "Q") or (i == 1 and type == "K"):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enimyColor and endPiece[1] == "N":
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        if self.whiteToMove:
            if self.board[r-1][c] == '--':
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == '--':
                        moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1), self.board))

            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+ 1), self.board))
        else:
            if self.board[r+1][c] == '--':
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r,c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == '--':
                        moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board))

            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r+1, c + 1), self.board))


        '''if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enimyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enimyColor = 'w'

        pawnProotion = False
        if self.board[r + moveAmount][c] == '--':
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow:
                    pawnProotion = True
                moves.append(Move((r, c), (r+moveAmount, c), self.board, pawnPromotion= pawnProotion))
                if r == startRow and self.board[r+2*moveAmount][c] == '--':
                    moves.append(Move((r,c), (r + 2*moveAmount, c),self.board))
            if c-1 >=0:
                if not piecePinned or pinDirection == (moveAmount, -1):
                    if self.board[r + moveAmount][c-1][0] == enimyColor:
                        if r +moveAmount == backRow:
                            pawnProotion = True
                        moves.append(Move((r, c),(r+moveAmount, c-1), self.board, pawnPromotion = pawnProotion))
                    if (r + moveAmount, c-1) == self.empassantPossible:
                        moves.append(Move((r,c), (r+moveAmount, c-1), self.board,enPassant=True))
            if c+1 <= 7 :
                if not piecePinned or pinDirection == (moveAmount, 1):
                    if self.board[r+moveAmount][c+1][0] == enimyColor:
                        if r + moveAmount == backRow:
                            pawnProotion = True
                        moves.append(Move((r, c), (r+moveAmount, c+1), self.board, pawnPromotion= pawnProotion))
                    if(r + moveAmount, c+1) == self.empassantPossible:
                        moves.append(Move((r, c), (r+ moveAmount, c+1), self.board, enPassant= True))'''

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        directons = ((-1, 0), (0,-1), (1,0), (0, 1)) #up, left, down, right,
        enimyColor = "b" if self.whiteToMove else "w"

        for d in directons:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (d[0], d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enimyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getknightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        playerColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow <8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != playerColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
    def getBisopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directons = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # up, left, down, right,
        enimyColor = "b" if self.whiteToMove else "w"
        for d in directons:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == '--':
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enimyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break


    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)

                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    if allyColor == "w":
                        self.whiteKingLocation = (r,c)
                    else:
                        self.blackKingLocation = (r, c)
        #self.getCastlingMoves(r, c, moves)

        '''kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0,-1), (0, 1), (1, -1), (1, 0), (1, 1))
        playerColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol <8 :
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != playerColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))'''
    def getCastlingMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, iscastleMove = True))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c-2] == '--' and self.board[r][c - 3]== '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c-2), self.board, iscastleMove = True))

    def getQueenMoves(self, r, c, moves):
        self.getBisopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs



class Move():
    ranksToRow = {"1":7, "2":6, "3":5, "4": 4, "5":3, "6":2, "7": 1, "8": 0}
    rowsToRank = {v:k for k , v in ranksToRow.items()}

    filesToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles={v:k for k, v in filesToCol.items()}

    def __init__(self, startSq, endSq, board, enPassant = False, iscastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.piececaptured = board[self.endRow][self.endCol]
        self.ispawnPromotion = False
        self.enPassant = enPassant
        #if enPassant:
           # self.piececaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'

        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.ispawnPromotion = True
        # Castle move
        self.iscastleMove = iscastleMove
        #self.isEmpassantMove = False
        #if self.pieceMoved[1] == 'p' and (self.endRow, self.endCol) == empassantPossible :
         #   self.isEmpassantMove = True'''
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRank[r]