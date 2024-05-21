#import ray
from mtcs import *

class Player:
    def __init__(self, color) -> None:
        self.color = color
    
    # Sistemare qui il valore che viene ritornato
    def make_move(self, game) -> None:
        if Go.get_empty_cells(game.board):
            mcts = MonteCarloTreeSearch(game.board)
            return mcts.get_move(game, self.color)
        return None