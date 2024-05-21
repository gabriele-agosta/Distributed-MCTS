import math
import copy
import random
import numpy as np

from node import *
from go import *


class MonteCarloTreeSearch():
    def __init__(self, board) -> None:
        self.root = Node(board)

    
    def get_move(self, game, color):
        for _ in range(100):
            leaf = self.selection(self.root)
            self.expansion(game, leaf, color)
            reward = self.simulation(color, leaf.board)
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
        for row in range(len(game.board)):
            for col in range(len(game.board[row])):
                if game.board[row][col] == [None]:
                    new_board = copy.deepcopy(game.board)
                    new_board[row][col] = color
                    node.children.append(Node(new_board, node, (row, col)))


    def simulation(self, color, board) -> int:
        current_color, captured_territory = color, None
        new_board = copy.deepcopy(board)
        passes = 0

        while passes < 2:
            row, cell = self.get_random_move(new_board)
            if row == -1 and cell == -1:
                passes += 1 
                continue
            new_board[row][cell] = current_color
            captured_territory = Go.white_captured_territory if color == "white" else Go.black_captured_territory
            Go.remove_captured_stones(new_board, color, captured_territory)
            current_color = Go.get_opposite_color(current_color)
        return Go.get_winner(new_board, color)
        
    
    def backpropagation(self, node, reward):
        while node is not None:
            node.n += 1
            node.t += reward
            node = node.parent


    def get_random_move(self, board):
        moves = Go.get_empty_cells(board)
        freedom_degrees = 0
        row, col = -1, -1
        while moves and freedom_degrees == 0:
            index = random.randint(0, len(moves) - 1)
            row, col = moves.pop(index)
            freedom_degrees =  Go.get_cell_freedom_degrees(board, row, col)
        return (row, col)

    
# Parallelizzare la simulazione della singola mossa