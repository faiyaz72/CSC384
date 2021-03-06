"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

maxCache = dict()
minCache = dict()
alphaMaxCache = dict()
alphaMinCache = dict()


def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state

def getOpponent(color):
    if (color == 1):
        return 2
    else:
        return 1

def compute_utility(board, color):

    # utility should be calculated as the number of disks of the player's colour minus the number of disks of the opponent
    # 1 is dark
    # 2 is light
    diskNum = get_score(board)
    if (color == 1):
        return diskNum[0] - diskNum[1]
    else:
        return diskNum[1] - diskNum[0]

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    #IMPLEMENT (and replace the line below)
    possibleMoves = get_possible_moves(board, getOpponent(color))
    minUtility = float("inf")
    bestMove = None

    if (possibleMoves == [] or limit == 0):
        return (bestMove, -1 * compute_utility(board, getOpponent(color)))

    bestMove = possibleMoves[0]
    for move in possibleMoves:
        moveBoard = play_move(board, getOpponent(color), move[0], move[1])
        utility = minimax_max_node(moveBoard, color, limit - 1, caching)[1]
        if (minUtility > utility):
            minUtility = utility
            bestMove = move

    return (bestMove, minUtility)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT (and replace the line below)
    
    possibleMoves = get_possible_moves(board, color)
    maxUtility = float("-inf")
    bestMove = None

    if (possibleMoves == [] or limit == 0):
        return (bestMove, compute_utility(board, color))

    bestMove = possibleMoves[0]
    for move in possibleMoves:
        moveBoard = play_move(board, color, move[0], move[1])
        utility = minimax_min_node(moveBoard, color, limit - 1, caching)[1]
        if (maxUtility < utility):
            maxUtility = utility
            bestMove = move

    return (bestMove, maxUtility)

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT (and replace the line below)
    return minimax_max_node(board, color, limit, caching)[0]

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    
    bestMove = None
    possibleMoves = get_possible_moves(board, getOpponent(color))
    minUtility = float("inf")

    if (caching == 1):
        if (isinstance(board, list)):
            board = tuple(tuple(x) for x in board)
        if ((board, getOpponent(color)) in alphaMinCache):
            return alphaMinCache[(board, getOpponent(color))]

    if (possibleMoves == [] or limit == 0):
        utilityScore = -1 * compute_utility(board, getOpponent(color))
        return (bestMove, utilityScore)

    if (ordering == 1):
        nodeOrderingList = []
        for move in possibleMoves:
            playBoard = play_move(board, getOpponent(color), move[0], move[1])
            nodeOrderingList.append((playBoard, move))
        
        nodeOrderingList.sort(key=lambda j: compute_utility(j[0], getOpponent(color)), reverse=True)

        for orderedMove in nodeOrderingList:
            utility = alphabeta_max_node(orderedMove[0], color, alpha, beta, limit - 1, caching, ordering)[1]
            if (minUtility > utility):
                minUtility = utility
                bestMove = orderedMove[1]
            if (minUtility <= alpha):
                return (bestMove, minUtility)
            beta = min(beta, minUtility)

    else:
        for move in possibleMoves:
            moveBoard = play_move(board, getOpponent(color), move[0], move[1])
            utility = alphabeta_max_node(moveBoard, color, alpha, beta, limit - 1, caching, ordering)[1]
            if (minUtility > utility):
                minUtility = utility
                bestMove = move
            if (minUtility <= alpha):
                return (bestMove, minUtility)
            beta = min(beta, minUtility)
    
    if (caching == 1):
        if (isinstance(board, list)):
            board = tuple(tuple(x) for x in board)
        alphaMinCache[(board, getOpponent(color))] = (bestMove, minUtility)
    return (bestMove, minUtility)
    

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    
    bestMove = None
    possibleMoves = get_possible_moves(board, color)
    maxUtility = float("-inf")

    if (caching == 1):
        if (isinstance(board, list)):
            board = tuple(tuple(x) for x in board)
        if ((board, color) in alphaMaxCache):
            return alphaMaxCache[(board, color)]

    if (possibleMoves == [] or limit == 0):
        utilityScore = compute_utility(board, color)
        return (bestMove, utilityScore)

    if (ordering == 1):
        nodeOrderingList = []
        for move in possibleMoves:
            playBoard = play_move(board, color, move[0], move[1])
            nodeOrderingList.append((playBoard, move))
        
        nodeOrderingList.sort(key=lambda j: compute_utility(j[0], color), reverse=True)

        for orderedMove in nodeOrderingList:
            utility = alphabeta_min_node(orderedMove[0], color, alpha, beta, limit - 1, caching, ordering)[1]
            if (maxUtility < utility):
                maxUtility = utility
                bestMove = orderedMove[1]
            if (maxUtility >= beta):
                return (bestMove, maxUtility)
            alpha = max(alpha, maxUtility)
    else:    
        for move in possibleMoves:
            moveBoard = play_move(board, color, move[0], move[1])
            utility = alphabeta_min_node(moveBoard, color, alpha, beta, limit - 1, caching, ordering)[1]
            if (maxUtility < utility):
                maxUtility = utility
                bestMove = move
            if (maxUtility >= beta):
                return (bestMove, maxUtility)
            alpha = max(alpha, maxUtility)
    
    if (caching == 1):
        if (isinstance(board, list)):
            board = tuple(tuple(x) for x in board)
        alphaMaxCache[(board, color)] = (bestMove, maxUtility)
    return (bestMove, maxUtility)


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT (and replace the line below)
    return alphabeta_max_node(board, color, float("-inf"), float("inf"), limit, caching, ordering)[0]

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
