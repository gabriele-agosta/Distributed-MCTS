import math
import copy
import random
import ray

from node import *
from go import *


class MonteCarloTreeSearch():
    def __init__(self, board) -> None:
        self.root = Node(board)

    
    def get_move(self, depth, game, player, opponent):
        for _ in range(depth):
            res = []

            leaf = self.selection(self.root)
            self.expansion(game, leaf, player.color)
            
            for child in leaf.children:
                res.append(self.simulation.remote(self, child.board, player, opponent))
            for reward in ray.get(res):
                self.backpropagation(leaf, reward)
        return self.best_child(self.root)
    

    def best_child(self, node):
        best_child = max(node.children, key=lambda child: child.n) if node.children else None
        return best_child
    
    
    def selection(self, node):
        while not node.is_leaf():
            node = self.best_ucb(node)
        return node


    def best_ucb(self, node):
        choices_weights = [self.upper_confidence_bound(child, node) for child in node.children]
        max_value = max(choices_weights)
        max_indices = [i for i, weight in enumerate(choices_weights) if weight == max_value]
        selected_index = random.choice(max_indices)
        return node.children[selected_index]
    

    def upper_confidence_bound(self, child, node) -> float:
        C = math.sqrt(2) 
        if child.n == 0:
            return float('inf')
        exploit_term = child.t / child.n
        explore_term = C * math.sqrt(math.log(node.n) / child.n)
        return exploit_term + explore_term
            

    def expansion(self, game, node, color):
        moves = []

        for row in range(len(game.board)):
            for col in range(len(game.board[row])):
                if game.board[row][col] == [None]:
                    moves.append((row, col))

        random.shuffle(moves)
        for i in range(min(10, len(moves))):
            row, col = moves[i]
            new_board = copy.deepcopy(game.board)
            new_board[row][col] = color
            node.children.append(Node(new_board, node, (row, col)))


    @ray.remote
    def simulation(self, board, player, opponent) -> int:
        current_color = player.color
        new_board = copy.deepcopy(board)
        passes = 0

        while passes < 2:
            row, cell = self.get_random_move(new_board, current_color, opponent)
            if row == -1 and cell == -1:
                passes += 1 
                continue
            new_board[row][cell] = current_color
            Go.check_region(new_board, player.color, opponent, (row, cell))
            current_color = Go.get_opposite_color(current_color)
        return Go.get_winner(new_board, player, opponent)
        
    
    def backpropagation(self, node, reward):
        while node is not None:
            node.n += 1
            node.t += reward
            node = node.parent


    def get_random_move(self, board, color, opponent):
        moves = Go.get_empty_cells(board)
        random.shuffle(moves)
        liberties, made_captures = 0, True
        row, col = -1, -1
        is_legit = (liberties != 0 or made_captures)

        while moves and not liberties:
            new_board = copy.deepcopy(board)
            row, col = moves.pop(0)
            new_board[row][col] = color
            liberties =  Go.get_cell_liberties(new_board, row, col)#, Go.check_suicide(new_board, (row, col), opponent)
            
        return (row, col)
