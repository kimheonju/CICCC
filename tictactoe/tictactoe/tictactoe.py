"""
Tic Tac Toe Player
"""

import math, copy

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
    num_x = sum([row.count(X) for row in board])
    num_o = sum([row.count(O) for row in board])
    return X if num_x <= num_o else O

  
def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions            


def result(board, action):
    
    new_board = [row[:] for row in board]

    # Check if the action is valid
    if not (0 <= action[0] < len(board) and 0 <= action[1] < len(board[0])):
        raise Exception("Invalid action: out of bounds")
    if board[action[0]][action[1]] is not None:
        raise Exception("Invalid action: cell already occupied")
    
    new_board[action[0]][action[1]] = player(board)
    
    return new_board



def winner(board):
    lines = [
        # Rows
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        # Columns
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        # Diagonals
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    
    for line in lines:
        if line[0] == line[1] == line[2] and line[0] is not None:
            return line[0]
    
    return None



def terminal(board):
    """
    Returns True if the game is over (either someone has won or all cells are filled), False otherwise.
    """
    # Check if there is a winner
    if winner(board) is not None:
        return True
    
    # Check if all cells are filled
    # the game is still in progress if there are empty cells
    if sum([row.count(EMPTY) for row in board]) > 0:
        return False
    
    return True
    
 
def utility(board):
    """
    Returns the utility of the board:
    1 if X has won, -1 if O has won, 0 if it's a tie.
    Assumes terminal(board) is True.
    """
    win = winner(board)
    if win == 'X':
        return 1
    elif win == 'O':
        return -1
    else:
        return 0



def max_value(board):
    """
    Returns the maximum value of a given board state for the MAX player (X).
    """
    if terminal(board):
        return utility(board)
    
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    """
    Returns the minimum value of a given board state for the MIN player (O).
    """
    if terminal(board):
        return utility(board)
    
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    best_action = None

    if current_player == 'X':
        best_value = float('-inf')
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
    else:  # current_player == 'O'
        best_value = float('inf')
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action

    return best_action
