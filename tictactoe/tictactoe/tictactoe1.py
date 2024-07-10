import math, copy

X = "X"
O = "O"
EMPTY = None

# Returns the initial state of the board. This function creates a 3x3 board with each cell set to EMPTY.
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# Returns the player who has the next turn on the board. It counts the number 
# of Xs and Os on the board and determines the player with fewer marks to be the next player.
def player(board):
    num_x = sum([row.count(X) for row in board])
    num_o = sum([row.count(O) for row in board])
    return X if num_x <= num_o else O

# Returns a set of all possible actions (i, j) available on the board. It collects all positions of empty cells.
def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions

# Returns the board that results from making move (i, j) on the board. This 
# function copies the board and places the current player's mark according to the given action.
def result(board, action):
    new_board = [row[:] for row in board]
    if not (0 <= action[0] < len(board) and 0 <= action[1] < len(board[0])):
        raise Exception("Invalid action: out of bounds")
    if board[action[0]][action[1]] is not None:
        raise Exception("Invalid action: cell already occupied")
    new_board[action[0]][action[1]] = player(board)
    return new_board

# Returns the winner of the game, if there is one. It checks all rows, columns, and diagonals for three consecutive marks and returns the winning mark.
def winner(board):
    lines = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    for line in lines:
        if line[0] == line[1] == line[2] and line[0] is not None:
            return line[0]
    return None

# Returns True if the game is over, False otherwise. The game is over if there is a winner or if there are no empty cells left.
def terminal(board):
    if winner(board) is not None:
        return True
    if sum([row.count(EMPTY) for row in board]) > 0:
        return False
    return True

# Returns the score of the current board. It assigns 1 for X win, -1 for O win, and 0 for a tie.
def utility(board):
    win = winner(board)
    if win == 'X':
        return 1
    elif win == 'O':
        return -1
    else:
        return 0

# These functions are the core of the minimax algorithm. max_value calculates the value to maximize for player X, and min_value calculates the value to 
# minimize for player O. They recursively explore all possible game states.
def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

# Uses the minimax algorithm to find the optimal next move. If the current 
# player is X, it uses max_value; if O, it uses min_value to determine the best action.
def minimax(board):
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
    else:
        best_value = float('inf')
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
    return best_action
