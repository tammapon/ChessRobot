import ChessEngine_W, CheesAI
from ChessEngine_W import Gamestate
from ChessEngine_W import *

def convert(s):
    lis = []
    lis[:0] = s

    return lis

def find_pos(lis):
    
    dict1 = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    a = dict1.get(lis[2])
    b = 8 - int(lis[3])
    return [b,a]

def find_pos1(lis):
    dict1 = {'1':7, '2':6, '3':5, '4':4, '5':3, '6':2, '7':1, '8':0}
    dict2 = {'h':7, 'g':6, 'f':5, 'e':4, 'd':3, 'c':2, 'b':1, 'a':0}
    a = dict2.get(lis[0])
    b = dict1.get(lis[1])
    c = dict2.get(lis[2])
    d = dict1.get(lis[3])
    return [a,b,c,d]
    

def is_occuppied(b, m):
    pos = find_pos(convert(m))
    # print(pos)
    # print(b[pos[0]][pos[1]])
    if b[pos[0]][pos[1]] == '--':
        return False
    return True

def tfMove(move):
    if move[1]=='1':
        if move[0]=='a':
            return (7,0)
        elif move[0]=='b':
            return (7,1)
        elif move[0]=='c':
            return (7,2)
        elif move[0]=='d':
            return (7,3)
        elif move[0]=='e':
            return (7,4)
        elif move[0]=='f':
            return (7,5)
        elif move[0]=='g':
            return (7,6)
        elif move[0]=='h':
            return (7,7)
    if move[1]=='2':
        if move[0]=='a':
            return (6,0)
        elif move[0]=='b':
            return (6,1)
        elif move[0]=='c':
            return (6,2)
        elif move[0]=='d':
            return (6,3)
        elif move[0]=='e':
            return (6,4)
        elif move[0]=='f':
            return (6,5)
        elif move[0]=='g':
            return (6,6)
        elif move[0]=='h':
            return (6,7)
    if move[1]=='3':
        if move[0]=='a':
            return (5,0)
        elif move[0]=='b':
            return (5,1)
        elif move[0]=='c':
            return (5,2)
        elif move[0]=='d':
            return (5,3)
        elif move[0]=='e':
            return (5,4)
        elif move[0]=='f':
            return (5,5)
        elif move[0]=='g':
            return (5,6)
        elif move[0]=='h':
            return (5,7)
    if move[1]=='4':
        if move[0]=='a':
            return (4,0)
        elif move[0]=='b':
            return (4,1)
        elif move[0]=='c':
            return (4,2)
        elif move[0]=='d':
            return (4,3)
        elif move[0]=='e':
            return (4,4)
        elif move[0]=='f':
            return (4,5)
        elif move[0]=='g':
            return (4,6)
        elif move[0]=='h':
            return (4,7)
    if move[1]=='5':
        if move[0]=='a':
            return (3,0)
        elif move[0]=='b':
            return (3,1)
        elif move[0]=='c':
            return (3,2)
        elif move[0]=='d':
            return (3,3)
        elif move[0]=='e':
            return (3,4)
        elif move[0]=='f':
            return (3,5)
        elif move[0]=='g':
            return (3,6)
        elif move[0]=='h':
            return (3,7)
    if move[1]=='6':
        if move[0]=='a':
            return (2,0)
        elif move[0]=='b':
            return (2,1)
        elif move[0]=='c':
            return (2,2)
        elif move[0]=='d':
            return (2,3)
        elif move[0]=='e':
            return (2,4)
        elif move[0]=='f':
            return (2,5)
        elif move[0]=='g':
            return (2,6)
        elif move[0]=='h':
            return (2,7)
    if move[1]=='7':
        if move[0]=='a':
            return (1,0)
        elif move[0]=='b':
            return (1,1)
        elif move[0]=='c':
            return (1,2)
        elif move[0]=='d':
            return (1,3)
        elif move[0]=='e':
            return (1,4)
        elif move[0]=='f':
            return (1,5)
        elif move[0]=='g':
            return (1,6)
        elif move[0]=='h':
            return (1,7)
    if move[1]=='8':
        if move[0]=='a':
            return (0,0)
        elif move[0]=='b':
            return (0,1)
        elif move[0]=='c':
            return (0,2)
        elif move[0]=='d':
            return (0,3)
        elif move[0]=='e':
            return (0,4)
        elif move[0]=='f':
            return (0,5)
        elif move[0]=='g':
            return (0,6)
        elif move[0]=='h':
            return (0,7)

def get_chess_board(ML_send_board):
    global x_box_now, y_box_now, x_box_go, y_box_go,status
 
    gs = Gamestate(ML_send_board)
    
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made
    running = True
    sqSelected = ()
    playerClicks = [] 
    gameOver = False
    playerOne = False   # player white if False = AI , True = Player
    playerTwo = True   # player black if False = AI , True = Player
    print(gs.board)
    while running:  
        humanTurn = (gs.whiteTomove and playerOne) or (not gs.whiteTomove and playerTwo)
        if not gameOver and humanTurn:
            print('form :')
            form = input()
            print('to :')
            to = input()
            form = tfMove(form)
            to = tfMove(to)
            move = ChessEngine_W.Move(form, to, gs.board)
            
            # print([playerClicks[0],playerClicks[1]])
            print("-----> Player Move <-----")
            print("Move_Position" , move.getChessNotation())
        
            for i in range(len(validMoves)):
                print('test')
                if move == validMoves[i]:
                    gs.makeMove(validMoves[i])
                    moveMade = True
                    if gs.send_castle() == "Castling1":
                        if gs.whiteTomove == False:
                            pass
                            # print("Castling W - R")
                    if gs.send_castle() == "Castling2":
                        if gs.whiteTomove == False:
                            pass
                            # print("Castling W - L")
                    if gs.send_castle() == "Castling1":
                        if gs.whiteTomove == True:
                            pass
                            # print("Castling B - R")
                    if gs.send_castle() == "Castling2":
                        if gs.whiteTomove == True:
                            pass
                            # print("Castling B - L")
            print(gs.board)        

    
        #AI move finder
        if not gameOver and not humanTurn:
            AIMove = CheesAI.findBestMove(gs, validMoves)
            pos_ai = ChessEngine_W.Move.getChessNotation(AIMove)
            
            # print(find_pos1(pos_ai))
            x_box_now = find_pos1(pos_ai)[1]
            y_box_now = find_pos1(pos_ai)[0]
            x_box_go = find_pos1(pos_ai)[3]
            y_box_go = find_pos1(pos_ai)[2]
            status = is_occuppied(gs.board, pos_ai)
            # print("pos_now = ",x_box_now,y_box_now," pos_go = ",x_box_go,y_box_go)
            print("Move_Position =", pos_ai)
            print("status =", status)
            # move_chess_2([x_box_now,y_box_now],[x_box_go,y_box_go],status)
            print("finish")
            if AIMove is None:
                AIMove = CheesAI.findRondomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            print(gs.board)


        if moveMade:
            validMoves = gs.getValidMoves()
    
            moveMade = False

        if gs.checkMate:
            gameOver = True
            if gs.whiteTomove:
                pass
                # drawText(screen, 'Black wins by checkMate')
            else:
                pass
                # drawText(screen, 'White wins by checkMate')
        elif gs.staleMate:
            gameOver = True
            # drawText(screen, 'staleMate')

# get_chess_board([["bR","bN","bB","bQ","bK","bB","bN","bR"],
#             ["bp","bp","bp","bp","bp","bp","bp","bp"],
#             ["--","--","--","--","--","--","--","--"],
#             ["--","--","--","--","--","--","--","--"],
#             ["--","--","--","--","--","--","--","--"],
#             ["--","--","--","--","--","--","--","--"],
#             ["wp","wp","wp","wp","wp","wp","wp","wp"],
#             ["wR","wN","wB","wQ","wK","wB","wN","wR"]])





