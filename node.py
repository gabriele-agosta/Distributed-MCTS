class Node:
    def __init__(self, board, parent=None, move=None, color=None):
        self.t = 0
        self.n = 0
        self.parent = parent
        self.board = board
        self.children = []
        self.move = move
        self.color = color


    def add_child(self, child) -> None:
        self.children.append(child)

    
    def is_leaf(self) -> bool:
        return len(self.children) == 0
