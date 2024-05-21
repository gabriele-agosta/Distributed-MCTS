#import ray
import numpy as np
import time

from player import *
from go import *

'''
    - Devo sistemare la simulazione
    - Devo sistemare come vengono gestiti i casi in cui non ci sono freedom degree e lascio la cella su None
    - Devo sistemare come viene calcolato il punteggio, assegnando le zone libere correttamente
'''

def check_move(board, node, color):
    if node == None:
        return True
    else:
        row, col = node.move
        board[row][col] = color
        captured = Go.white_captured_territory if color == "white" else Go.black_captured_territory
        Go.remove_captured_stones(board, color, captured)
        return False


def start_game(game, white, black):
    skip_turn = [False, False]
    while not all(skip_turn):
        move = black.make_move(game)
        skip_turn[1] = check_move(game.board, move, black.color)
        game.print_board()
        node = white.make_move(game)
        skip_turn[0] = check_move(game.board, node, white.color)
        game.print_board()
    return game.get_winner(game.board, white.color)


def main():
    n = int(input("Choose the dimension of the board (n x n): "))
    game = Go(n)
    white, black = Player("white"), Player("black")

    winner = start_game(game, white, black)
    res = "White" if winner == 1 else "Black"
    print(f"Result: { res } won!\n") 


if __name__ == "__main__":
    main()
