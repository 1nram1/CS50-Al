"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def check_all_empty(sublist):
    return all(element == EMPTY for element in sublist)
    

def check_all_not_empty(sublist):
    return all(element != EMPTY for element in sublist)
   

def check_empty(board):
    return all(check_all_empty(sublist) for sublist in board)

def check_not_empty(board):
    return all(check_all_not_empty(sublist) for sublist in board)

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x ,count_o = 0, 0

    #貌似直接数个数就足够了，不需要去单独考虑全空和全满的情况
    # if check_empty(board) or check_not_empty(board):
    #     return X
    for sublist in board:
        for element in sublist:
            if element == X:
                count_x += 1
            elif element == O:
                count_o += 1
    if count_x > count_o :
        return O
    else:
        return X
    
            
        

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    其实就是返回你要下的棋的坐标,i为第几行为第几列
    """
    emptyplace = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                emptyplace.add((i,j))
    return emptyplace
    

import copy

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]

    copy_board = copy.deepcopy(board)

    if i >= 0 and i <= 2 and j >= 0 and j <= 2 and board[i][j] == EMPTY:
        this_player = player(copy_board)
        copy_board[i][j] = this_player
        return copy_board
    raise Exception("infeasible move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2]) and board[i][0] != EMPTY:
            return board[i][0]
        if (board[0][i] == board[1][i] == board[2][i]) and board[0][i] != EMPTY:
            return board[0][i]
    if ((board[0][0] == board[1][1] == board[2][2]) and board[0][0] != EMPTY) or ((board[0][2] == board[1][1] == board[2][0]) and board[1][1] != EMPTY):
        return board[1][1]
    return None
    
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if check_not_empty(board) or winner(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def max_value(board):
    if terminal(board):
        return (utility(board),None)
    value = float('-inf')
    action_to_take = None
    for action in actions(board):
        v = min_value(result(board,action))[0]
        if v > value:
            value = v 
            action_to_take = action
            solution = (value,action_to_take)
    return solution

def min_value(board):
    if terminal(board):
        return (utility(board),None)
    value = float('inf')
    action_to_take = None
    for action in actions(board):
        v = max_value(result(board,action))[0]
        if v < value:
            value = v 
            action_to_take = action
            solution = (value,action_to_take)
    return solution

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    this_player = player(board)
    if this_player == X :
        return max_value(board)[1]
    else:
        return min_value(board)[1]

