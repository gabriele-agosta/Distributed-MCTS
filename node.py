class Node:
    def __init__(self, board, parent=None, move=None):
        self.t = 0
        self.n = 0
        self.parent = parent
        self.board = board
        self.children = []
        self.move = move


    def add_child(self, child):
        self.children.append(child)

    
    def is_leaf(self):
        return len(self.children) == 0
