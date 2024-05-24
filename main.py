from player import *
from go import *

'''
    - ( ) Devo sistemare come viene selezionata una move. Attualmente mi sembra che sto creando un albero, ma espando solamente un nodo tra i figli di ognuno
    - (X) Devo sistemare come vengono gestiti i casi in cui non ci sono freedom degree e lascio la cella su None
    - (X) Devo sistemare come viene calcolato il punteggio, assegnando le zone libere correttamente
'''

def check_move(board, node, color, opponent):
    if node == None:
        return True
    else:
        row, col = node.move
        board[row][col] = color
        captured = Go.white_captured_territory if color == "white" else Go.black_captured_territory
        Go.remove_captured_stones(board, color, captured, opponent)
        return False


def start_game(game, white, black):
    skip_turn = [False, False]
    while not all(skip_turn):
        move = black.make_move(game, white)
        skip_turn[1] = check_move(game.board, move, black.color, white)
        game.print_board()
        node = white.make_move(game, black)
        skip_turn[0] = check_move(game.board, node, white.color, black)
        game.print_board()
    return game.get_winner(game.board, white, black)


def main():
    n = int(input("Choose the dimension of the board (n x n): "))
    game = Go(n)
    white, black = Player("white"), Player("black")

    winner = start_game(game, white, black)
    res = "White" if winner == 1 else "Black"
    print(f"Result: { res } won!\n") 


if __name__ == "__main__":
    main()
