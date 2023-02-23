import random
import time
import sys
import ChessEngine


pieceScore = {"K": 100, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4

Average_time = 0
Round = 0

def findRondomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

'''
Helper method to make first recursive call
'''
def findBestMove(gs, validMoves):
    global nextMove, counter, Average_time, Round
    start_time = time.time()
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteTomove else -1)   # use original
    
    
    Average_time += time.time() - start_time
    Round += 1
    print("-----> AI Move <-----")
    print("Round %s" % (Round))
    print("%s Seconds" % (time.time() - start_time))
    # print("Average time = %s" % (Average_time/Round))
    # print(gs.board)
    
    return nextMove



def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        # print("-------------->", move )
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undomove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break

    return maxScore

def scoreBoard(gs):
    # print(gs.board + ",")
    if gs.checkMate:
        if gs.whiteTomove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            
            if square[0] == 'w':
                score += pieceScore[square[1]]
                # print(str(score)+ "w")
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
                # print(str(score)+ "b")

    return score


'''
Score the board based on material.
'''
def scoreMaterial(board):
    score = 0
    
    for row in board:
        # print(row + ",")
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
                # print(str(score) + "w") 
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
                # print(str(score) + "b")

    return score

