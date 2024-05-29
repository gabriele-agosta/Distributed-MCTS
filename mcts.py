import math
import copy
import random
import ray

from node import *
from go import *


class MonteCarloTreeSearch():
    def __init__(self, board) -> None:
        self.root = Node(board)

    
    def get_move(self, iterations, game, player, opponent):
        p1, p2 = player, opponent
        for _ in range(iterations):
            res = []

            leaf = self.selection(self.root)
            self.expansion(game, leaf, 10, p1.color)
            
            for child in leaf.children:
                res.append(self.simulation.remote(self, child.board, p1, p2))
            for reward in ray.get(res):
                self.backpropagation(leaf, reward)
            p1, p2 = p2, p1
        return self.best_child(self.root)
    

    def best_child(self, node):
        best_child = max(node.children, key=lambda child: child.n) if node.children else None
        return best_child
    
    
    def selection(self, node):
        while not node.is_leaf():
            node = self.uct(node)
        return node


    def uct(self, node):
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
            

    def expansion(self, game, node, n_children, color):
        moves = Go.get_empty_cells(game.board, color)

        random.shuffle(moves)
        for i in range(min(n_children, len(moves))):
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
            row, cell = self.get_random_move(new_board, player.color)
            if row == -1 and cell == -1:
                passes += 1 
                continue
            new_board[row][cell] = current_color
            Go.manage_regions(new_board, player, opponent)
            current_color = Go.get_opposite_color(current_color)
        return Go.get_winner(new_board, player, opponent)
        
    
    def backpropagation(self, node, reward):
        while node is not None:
            node.n += 1
            node.t += reward
            node = node.parent


    def get_random_move(self, board, color):
        moves = Go.get_empty_cells(board, color)
        random.shuffle(moves)
        row, col = moves.pop(0) if moves else (-1, -1)
            
        return (row, col)
