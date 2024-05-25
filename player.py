from mtcs import *

class Player:
    def __init__(self, color) -> None:
        self.color = color
        self.captures = 0
    
    # Sistemare qui il valore che viene ritornato
    def make_move(self, depth, game, opponent) -> None:
        if Go.get_empty_cells(game.board):
            mcts = MonteCarloTreeSearch(game.board)
            return mcts.get_move(depth, game, self, opponent)
        return None