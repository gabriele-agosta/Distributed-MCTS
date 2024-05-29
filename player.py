from mcts import *
from node import *
from typing import Optional


class Player:
    def __init__(self, color) -> None:
        self.color = color
        self.captures = 0
    

    def make_move(self, depth, game, opponent) -> Optional[Node]:
        if Go.get_empty_cells(game.board, self.color):
            mcts = MonteCarloTreeSearch(game.board)
            return mcts.get_move(depth, game, self, opponent)
        return None