from player import *
from go import *

'''
    - ( ) Devo sistemare come viene selezionata una move. Attualmente mi sembra che sto creando un albero, ma espando solamente un nodo tra i figli di ognuno
    - ( ) Devo sistemare come viene selezionata una move. Devo consentire di posizionare dove non ci sono gradi di libertà se però si riesce a fare una cattura
'''

def check_move(board, node, color, opponent):
    if node == None:
        return True
    else:
        row, col = node.move
        board[row][col] = color
        Go.check_region(board, color, opponent)
        return False


def start_game(game, white, black):
    skip_turn = [False, False]
    while not all(skip_turn):
        move = black.make_move(10, game, white)
        skip_turn[1] = check_move(game.board, move, black.color, white)
        game.print_board()
        node = white.make_move(10, game, black)
        skip_turn[0] = check_move(game.board, node, white.color, black)
        game.print_board()
    return game.get_winner(game.board, white, black)


def main():
    n = int(input("Choose the dimension of the board (n x n): "))
    game = Go(n)
    white, black = Player("white"), Player("black")

    winner = start_game(game, white, black)
    res = "White" if winner == 1 else "Black"
    game.print_board()
    print(f"\n\nResult: { res } won!\n") 


if __name__ == "__main__":
    main()
