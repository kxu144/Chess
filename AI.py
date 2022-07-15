from copy import deepcopy
from Chess import *

def eval_position(board): # naive eval
    score = 0
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece.piece:
                score += piece.color * Chess.piece_values[type(piece)]
    return score

def alpha_beta(chess, depth, alpha, beta, player):
    board = chess.board
    if chess.in_checkmate(player):
        return player * float('inf')
    if depth == 0:
        return eval_position(board, player)

    if player == 1:
        value = float('-inf')
        for move in chess.display_available_moves(board):
            new_board = deepcopy(board)
            chess.move(new_board, move)
            value = max(value, alpha_beta(chess, depth - 1, alpha, beta, -player))
            if value >= beta:
                break
            alpha = max(alpha, value)
        return value
    else:
        value = float('inf')
        for move in chess.display_available_moves(board):
            new_board = deepcopy(board)
            chess.move(new_board, move)
            value = min(value, alpha_beta(chess, depth - 1, alpha, beta, -player))
            if value <= alpha:
                break
            beta = min(beta, value)
        return value
