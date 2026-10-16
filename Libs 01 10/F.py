import numpy as np

def checkerboard(n):
    board = np.zeros((n, n), dtype=int)
    board[0:n:2, 1:n:2] = 1
    board[1:n:2, 0:n:2] = 1
    return board
