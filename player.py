from typing import Union

from mtcs import *

class Player:
    def __init__(self, color) -> None:
        self.color = color
        self.prev_move = ()
    

    def make_move(self, game) -> Union[None, Node]:
        if Go.get_empty_cells(game.board):
            mcts = MonteCarloTreeSearch(game.board)
            return mcts.get_move(game, self.color, self.prev_move)
        return None