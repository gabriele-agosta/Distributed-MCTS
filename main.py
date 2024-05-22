from player import *
from go import *

'''
    - Devo vedere esattamente se è giusto che vengano eseguite tutte le operazioni del MCTS 100 volte (secondo me sì)
    - Devo sistemare come vengono gestiti i casi in cui non ci sono freedom degree e lascio la cella su None
    - Devo sistemare come viene calcolato il punteggio, assegnando le zone libere correttamente 
'''

def check_move(board, node, player):
    if node == None:
        return True
    else:
        row, col = node.move
        board[row][col] = player.color
        player.prev_move = (row, col)
        captured = Go.white_captured_territory if player.color == "white" else Go.black_captured_territory
        Go.remove_captured_stones(board, player.color, captured)
        return False


def start_game(game, white, black):
    skip_turn = [False, False]

    while not all(skip_turn):
        move = black.make_move(game)
        skip_turn[1] = check_move(game.board, move, black)
        Go.print_board(game.board)
        node = white.make_move(game)
        skip_turn[0] = check_move(game.board, node, white)
        Go.print_board(game.board)
    return game.get_winner(game.board, white.color)


def main():
    n = int(input("Choose the dimension of the board (n x n): "))
    game = Go(n)
    white, black = Player("white"), Player("black")

    winner = start_game(game, white, black)
    Go.print_board(game.board)
    res = "White" if winner == 1 else "Black"
    print(f"Result: { res } won!\n") 


if __name__ == "__main__":
    main()
