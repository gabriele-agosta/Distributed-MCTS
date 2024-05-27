from player import *
from go import *


def check_move(board, node, player, opponent) -> bool:
    if node == None:
        return True
    else:
        row, col = node.move
        board[row][col] = player.color
        Go.manage_regions(board, player, opponent)
        return False


def start_game(game, white, black) -> int:
    skip_turn = [False, False]
    white_iterations, black_iterations = 10, 10

    while not all(skip_turn):
        move = black.make_move(black_iterations, game, white)
        skip_turn[1] = check_move(game.board, move, black, white)
        game.print_board()
        node = white.make_move(white_iterations, game, black)
        skip_turn[0] = check_move(game.board, node, white, black)
        game.print_board()
    return game.get_winner(game.board, white, black)


def main() -> None:
    n = int(input("Choose the dimension of the board (n x n): "))
    game = Go(n)
    white, black = Player("white"), Player("black")

    winner = start_game(game, white, black)
    res = "White" if winner == 1 else "Black"
    game.print_board()
    print(f"\n\nResult: { res } won!\n") 


if __name__ == "__main__":
    main()
