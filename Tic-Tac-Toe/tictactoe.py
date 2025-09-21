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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    countX = 0
    countO = 0
    
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                countX += 1
            if board[row][col] == O:
                countO += 1
    
    if countX > countO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                actions.add((row, col))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    row, col = action
    
    if board[row][col] != EMPTY:
        raise Exception("Invalid action")
    elif row < 0 or row > 2 or col < 0 or col > 2:
        raise Exception("Invalid action")
    else:
        result_board = [linha[:] for linha in board]
        result_board[row][col] = current_player
        return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # checking all rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]
        
    # checking all columns
    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]    
        
    # checking first digonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    
    # checking second diagonal
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2] 
    
    return None    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    check_actions = actions(board)
    check_winning = winner(board)
    
    if len(check_actions) == 0 or check_winning != None:
        return True
    else: 
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    check_terminal = terminal(board)
    
    if check_terminal:
        win = winner(board)
        if win == X:
            return 1
        elif win == O:
            return -1
        else:
            return 0 


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    def maxValue(state):
        if terminal(state):
            return None, utility(state)
        best_action = None
        v = float("-inf")
        for action in actions(state):
            min_action, min_value = minValue(result(state, action))
            if min_value > v:
                v = min_value
                best_action = action
        return best_action, v      
            
    def minValue(state):
        if terminal(state):
            return None, utility(state)
        best_action = None
        v = float("inf")
        for action in actions(state): 
            max_action, max_value = maxValue(result(state, action))
            if max_value < v:
                v = max_value
                best_action = action
        return best_action, v  
    
    if player(board) == X:
        move, value = maxValue(board)
        return move
    else:
        move, value = minValue(board)
        return move
