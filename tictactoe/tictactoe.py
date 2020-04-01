"""
Tic Tac Toe Player
"""

import math
import copy

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
    xc = 0
    oc = 0

    for row in board:
        xc += row.count(X)
        oc += row.count(O)

    if xc > oc:
        return O
    elif xc == oc:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.append((i, j))
    
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    the_player = player(board)
    i, j = action
    new_board[i][j] = the_player

    return new_board


def winner_by_row(custom_board):
    """
    return (True/False, winner).
    """

    # winner by row
    for row in custom_board:
        winX = True
        winO = True

        for cell in row:
            winX &= (cell == X)
            winO &= (cell == O)
        
        if winX:
            return (True, X)
        elif winO:
            return (True, O)
    
    return (False, EMPTY)


def transpose(board):
    """
    Transpose of a board
    """

    return [ 
        [ board[j][i] for j in range(len(board)) ]
        for i in range(len(board))
    ]


def terminal_winner(board):
    """
    return (True/False, winner).
    if non termianal, winner may be anything
    """

    # winner by row
    terminal, winner = winner_by_row(board)
    if terminal:
        return (terminal, winner)
    
    # winner by col.
    terminal, winner = winner_by_row(transpose(board))
    if terminal:
        return (terminal, winner)
    
    # winner by diagonal
    main_diagonal = []
    for i in range(len(board)):
        main_diagonal.append(board[i][i])
    
    secondary_diagonal = []
    for i in range(len(board)):
        secondary_diagonal.append(board[i][len(board) - 1 - i])

    terminal, winner = winner_by_row([main_diagonal, secondary_diagonal])
    if terminal:
        return (terminal, winner)

    # tie
    done = True
    for row in board:
        for cell in row:
            done &= cell != EMPTY
    
    if done:
        return (True, None)


    # non terminal
    return (False, None)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    terminal, winner = terminal_winner(board)

    if terminal:
        return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    terminal, winner = terminal_winner(board)

    return terminal


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    terminal, winner = terminal_winner(board)

    if winner == X:
        return 1
    elif winner == O:
        return -1
    else:
        return 0


def maxValue(board):
    if terminal(board):
        return utility(board), None
    
    m = - math.inf
    
    for action in actions(board):
        mx, tx = minValue(result(board, action))
        if mx > m:
            act = action
            m = mx
    
    return m, act


def minValue(board):
    
    if terminal(board):
        return utility(board), None
    
    m = math.inf
    for action in actions(board):
        mx, tx = maxValue(result(board, action))
        if mx < m:
            m = mx
            act = action
    return m, act

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if player(board) == X:
        return maxValue(board)[1]
    else:
        return minValue(board)[1]
