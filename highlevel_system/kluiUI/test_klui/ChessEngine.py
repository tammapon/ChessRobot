

from asyncio.windows_events import NULL
from cgi import test
from copyreg import constructor





class Gamestate():
    def __init__(self, board):

        self.board = board
        self.prev = 0
        self.current = 0
        
        self.moveFunctions = {'p': self.getPawnMoves, "R": self.getRookMoves, 'N': self.getKnightMoves, 
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        
        self.whiteTomove = True
        self.moveLog = [] 
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []  
        self.checks = []
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        self.playerOne = False   # player white if False = AI , True = Player
        self.playerTwo = False     # player black if False = AI , True = Player

        self.currentCastlingRight = CastleRights(True,True,True,True)
        self.CastleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                self. currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

        self.check_stal = 'a'

    '''
    takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passent)
    '''
    
    
    
    def makeMove(self, move):
        
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) 
        self.whiteTomove = not self.whiteTomove  #swap player
        # update the king's location if moved
        if move.pieceMoved == 'wK' :
            self.whiteKingLocation = (move.endRow, move.endCol)
            
            
        elif move.pieceMoved == 'bK' :
            self.blackKingLocation = (move.endRow, move.endCol)
        

        #if pawn moves twice, next move can capture enpassant
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPosible = ((move.endRow + move.startRow)//2, move.endCol)
           
        # else:
            self.enpassantPosible= ()
            

        # enpassant move
        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"
            

#-------------------------------------------------------------
        #update enpassantpossible variable
#         if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
#             self.enpassantPosible = ((move.startRow + move.endRow)//2, move.startCol)
#         else:
#             self.enpassantPosible = ()                            
# #-------------------------------------------------------------
        #pawn promotion 
        if move.pawnPromotion:
           
            if self.playerOne == True & self.playerTwo == True :
                promotedPiece = input("Promote to Q, R, B, or N:")
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece
            if self.playerOne == False & self.playerTwo == False :
                promotedPiece = "Q"
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece
            
        
        #castle move
        if move.isCastleMove:
            # print("--------- Castling0")
            if move.endCol - move.startCol == 2: #kingside castle move
                self.check_stal = "Castling1"
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] # moves the rook
                self.board[move.endRow][move.endCol+1] = '--' #erase old rook
            else: #queen side castle
                self.check_stal = "Castling2"
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] # moves the rook
                self.board[move.endRow][move.endCol-2] = '--'


        #update castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.CastleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                                self. currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        
        
    def send_castle(self):
        return self.check_stal
        
    

    '''
    Undo the last move made
    '''
    def undomove(self):
        
        if len(self.moveLog) != 0: # make sure that there is a move to undo
            
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteTomove = not self.whiteTomove # switch turns back 
            # update the king's location if moved
            if move.pieceMoved == 'wK' :
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK' :
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo en passant
            if move.enPassant:
              
                self.board[move.endRow][move.endCol] == '--' #leave landing square blank
                self.board[move.startRow][move.endCol] == move.pieceCaptured
                self.enpassantPosible = (move.endRow, move.endCol)
            # undo 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPosible = ()

            # undo castle rights
            self.CastleRightsLog.pop()
            newRights = self.CastleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1] # move rook
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1] # move rook
                    self.board[move.endRow][move.endCol+1] = '--'
            # ADD THESE
            self.checkMate = False
            self.staleMate = False
        

    '''
    Update the castle rights given the move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK' :
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

            

            

    # All move considering check
    # def getValidMoves(self):
    #     tempEnpassantPossible = self.enpassantPosible
    #     moves = []
    #     self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
    #     if self.whiteTomove:
    #         kingRow = self.whiteKingLocation[0]
    #         kingCol = self.whiteKingLocation[1]
    #     else:
    #         kingRow = self.blackKingLocation[0]
    #         kingCol = self.blackKingLocation[1]
    #     if self.inCheck:
    #         if len(self.checks) == 1:
    #             moves = self.getAllPossibleMoves()

    #             check = self.checks[0]
    #             checkRow = check[0]
    #             checkCol = check[1]
    #             pieceChecking = self.board[checkRow][checkCol]
    #             validSquares = []

    #             if pieceChecking[1] == 'N':
    #                 validSquares = [(checkRow, checkCol)]
    #             else:
    #                 for i in range(1, 8):
    #                     validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
    #                     validSquares.append(validSquare)
    #                     if validSquares[0] == checkRow and validSquares[1] == checkCol:
    #                         break

    #             for i in range(len(moves)-1, -1, -1):
    #                 if moves[i].pieceMoved[1] != "K":
    #                     if not (moves[i].endRow, moves[i].endCol) in validSquares:
    #                         moves.remove(moves[i])
    #         else:
    #             self.getKingMoves(kingRow, kingCol, moves)
    #     else:
    #         moves = self.getAllPossibleMoves()
            
    #     if len(moves) == 0:
    #        self.checkMate = True
    #     else:
    #         self.checkMate = False
    #         self.staleMate = False
        
    #     self.enpassantPosible = tempEnpassantPossible
    #     return moves

    def getValidMoves(self): 
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteTomove:
          
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
          
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
          
            if len(self.checks) == 1: # only 1 check, block check or move king 

                moves = self.getAllPossibleMoves()
                # to block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0] #check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #enemy piece causing the check
                validSquares = [] #squares that pieces can move to
                # if knigt, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow,checkCol)]
                else: 
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) #check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #once you get to piece end checks
                            break
                
                #get rid of any moves that don't block check or move king
                for i in range(len(moves) -1, -1, -1): #go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != 'K': # move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: #double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        
        # if self.whiteTomove:
        #     self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        # else:
        #     self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        
        if len(moves) == 0:
            if self.inCheckFunction():
              
                self.checkMate = True
            else:
               
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        
        # self.enpassantPossible = tempEnpassantPossible
        # self.currentCastlingRight = tempCastleRights
        return moves
        # tempEnpassantPossible = self.enpassantPosible
        # #1.) generate all possible moves
        # moves = self.getAllPossibleMoves()
        # # 2.) for each move, make the move
        # for i in range(len(moves)-1, -1, -1):
        #     self.makeMove(moves[i])
        #     # 3.) generate all opponent's moves
        #     # 4.) for each of your opponent's move, see if they attack your king
        #     self.whiteTomove = not self.whiteTomove
        #     if self.inCheck():
        #         moves.remove(moves[i])  #5.) if thry do attack your king, not avalid move
        #     self.whiteTomove = not self.whiteTomove
        #     self.undomove()
        # if len(moves) == 0:
        #     if self.inCheck():
        #         self.checkMate = True
        #     else:
        #         # self.checkMate = False
        #         self.staleMate = True
        
        # self.enpassantPosible = tempEnpassantPossible
        # return moves

    '''
    Determine if the current player is in check
    '''
    def inCheckFunction(self):
        if self.whiteTomove:
         
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
          
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    
    '''
    Determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteTomove = not self.whiteTomove #switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteTomove = not self.whiteTomove #switch turns back
        for move in oppMoves:
            # print(move.endRow,move.endCol)
            if move.endRow == r and move.endCol == c: #square is under attack
    
                return True
        return False

   
                    
            
    # All moves without considering check
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols in given row
                ture = self.board[r][c][0]
                if (ture == 'w' and self.whiteTomove) or (ture == 'b' and not self.whiteTomove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #calls the approprpiate move funcetion based on piece type
                   
        return moves

    #Get all the pawn moves for the pawn located at row, col and add these moves to the list
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
             
                break

        if self.whiteTomove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
        pawnPromotion = False

        if self.board[r + moveAmount][c] == '--': #1 square move
            if not piecePinned or pinDirection == (moveAmount,0):
                if r+moveAmount == backRow: # if piece gets to bank rank then it is a paen promotion
                    pawnPromotion = True
                moves.append(Move((r, c), (r+moveAmount,c), self.board, pawnPromotion=pawnPromotion))
                if r == startRow and self.board[r+ 2 * moveAmount][c] == '--': #2squre moves
                    moves.append(Move((r, c), (r+2 * moveAmount, c), self.board))

        if c-1 >= 0: # capture to left
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r+moveAmount][c-1][0] == enemyColor:
                    if r+moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r+moveAmount, c-1), self.board, pawnPromotion=pawnPromotion))
                if (r+moveAmount, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+moveAmount, c-1), self.board, enPassant=True))
        if c+1 <= 7: # capture to right
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r+moveAmount][c+1][0] == enemyColor:
                    if r+moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r+moveAmount, c+1), self.board, pawnPromotion=pawnPromotion))
                if (r+moveAmount, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+moveAmount, c+1), self.board, enPassant=True)) 




        # if self.whiteTomove: #white pawn moves
        #     if self.board[r-1][c] == "--": #1 square pawn advance
        #         if not piecePinned or pinDirection == (-1, 0):
        #             moves.append(Move((r, c), (r-1, c), self.board)) 
        #         if r == 6 and self.board[r-2][c] == "--":   #2 square pawn advance
        #             moves.append(Move((r, c), (r-2, c), self.board)) 
        #     if c-1 >= 0: #captures to the left
        #         if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
        #             if not piecePinned or pinDirection == (-1, -1):
        #                 moves.append(Move((r, c), (r-1, c-1), self.board)) 
        #             elif (r-1, c-1) == self.enpassantPosible:
        #                 moves.append(Move((r,c), (r-1, c-1), self.board, enpassantPosible = True))

        #     if c+1 <= 7: #capture to the right
        #         if self.board[r-1][c+1][0] == 'b': #enemy piece to capture
        #             if not piecePinned or pinDirection == (-1, 1):
        #                 moves.append(Move((r, c), (r-1, c+1), self.board)) 
        #             elif (r-1, c+1) == self.enpassantPosible:
        #                 moves.append(Move((r,c), (r-1, c+1), self.board, enpassantPosible = True))

        # else: #black pawn moves 
        #     if self.board[r+1][c] == "--": #1 square pawn advance
        #         # if not piecePinned or pinDirection == (1, 0):
        #         moves.append(Move((r, c), (r+1, c), self.board)) 
        #         if r == 1 and self.board[r+2][c] == "--":   #2 square pawn advance
        #             moves.append(Move((r, c), (r+2, c), self.board)) 
        #     if c-1 >= 0: #captures to the left
        #         if self.board[r+1][c-1][0] == 'w': #enemy piece to capture
        #             # if not piecePinned or pinDirection == (1, -1):
        #             moves.append(Move((r, c), (r+1, c-1), self.board)) 
        #         elif (r+1, c-1) == self.enpassantPosible:
        #             moves.append(Move((r,c), (r+1, c-1), self.board, enpassantPosible = True))
        #     if c+1 <= 7: #capture to the right
        #         if self.board[r+1][c+1][0] == 'w': #enemy piece to capture
        #             # if not piecePinned or pinDirection == (1, 1):
        #             moves.append(Move((r, c), (r+1, c+1), self.board)) 
        #         elif (r+1, c+1) == self.enpassantPosible:
        #             moves.append(Move((r,c), (r+1, c+1), self.board, enpassantPosible = True))

    #Get all the rook moves for the rook located at row, col and add these moves to the list
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        
        directions = ((-1,0), (0,-1), (1,0), (0,1)) # up, left, down, right 
        enemyColor = "b" if self.whiteTomove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPicec = self.board[endRow][endCol]
                        if endPicec == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPicec[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
                            break
                else: # off board
                    break



     #Get all the Knight moves for the Knight located at row, col and add these moves to the list
    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteTomove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                        moves.append(Move((r, c), (endRow, endCol), self.board))


     #Get all the Bishop moves for the Bishop located at row, col and add these moves to the list
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1,-1), (-1,1), (1,-1), (1,1)) #4 diaganols
        enemyColor = "b" if self.whiteTomove else "w"
        for d in directions:
            for i in range(1,8): # bishop can move max of 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # is it on board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPicec = self.board[endRow][endCol]
                        if endPicec == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPicec[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece invalid
                            break
                else: # off board
                    break


     #Get all the Queen moves for the Queen located at row, col and add these moves to the list
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

     #Get all the King moves for the King located at row, col and add these moves to the list
    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteTomove else "b"
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
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)



    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteTomove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        # check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol] 
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]

                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or\
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                           
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
                    if endPiece[0] == enemyColor and endPiece[1] == 'N':
                        inCheck = True
                        checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    
    '''
    Generate all valid castle moves for the king at (r,c) and add them to the list of moves
    '''
    # def getCastleMoves(self, r, c, moves):
    #     if self.squareUnderAttack(r, c):
    #         return #can't castle while we are in check
    #     if (self.whiteTomove and self.currentCastlingRight.wks) or (not self.whiteTomove and self.currentCastlingRight.bks):
    #         self.getKingsideCastleMoves(r, c, moves)
    #     if (self.whiteTomove and self.currentCastlingRight.wqs) or (not self.whiteTomove and self.currentCastlingRight.bqs):
            
    #         self.getQueensideCastleMoves(r, c, moves)
        
    # def getKingsideCastleMoves(self, r, c, moves):
    #     if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
    #         if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
    #             moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))
            
    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3]:
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))
                      
class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8":0 }
    rowToRanks  = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in  filesToCols.items()}

    def __init__(self, startSq, endSq, board, enPassant=False, pawnPromotion = False,isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow   = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.pawnPromotion = pawnPromotion
        self.isCastleMove = isCastleMove
        self.enPassant = enPassant
        if self.enPassant:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

        #pawn promotion 
        # self.pawnPromotion =  (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)

        #en passant
        # self.enPassant = enPassant
        # if self.enPassant:
        #     self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
    
        


        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
       
        

    #Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        #you could make this real chess notation , will just record the squares is rank/file notation
        # return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        ranksToRows = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
        rowsToRanks = {i:j for j,i in ranksToRows.items()}
        filesToCols = {'h':7, 'g':6, 'f':5, 'e':4, 'd':3, 'c':2, 'b':1, 'a':0}
        colsToFiles = {i:j for j,i in filesToCols.items()}
        return colsToFiles[c] + rowsToRanks[r]
    
    

