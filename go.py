from typing import List, Tuple


class Go():
    def __init__(self, n) -> None:
        self.board = [[ [None] for _ in range(n) ] for _ in range(n)]


    def print_board(self) -> None:
        print("\n\n")
        for row in self.board:
            for cell in row:
                if cell == "white":
                    print("\U000026AA", end=" ")
                elif cell == "black":
                    print("\U000026AB", end=" ")
                elif cell == [None]:
                    print("\U0001F7E7", end=" ")
                else:
                    print(cell, end=" ")
            print()


    @staticmethod
    def map_regions(board, player, opponent) -> List[Tuple[int, int]]:
        visited = [[False for _ in range(len(board))] for _ in range(len(board))]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        regions = []

        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] in [player.color, opponent.color] and not visited[row][col]:
                    curr_color = player.color if board[row][col] == player.color else opponent.color
                    stack = [(row, col)]
                    region = set()

                    while stack:
                        r, c = stack.pop()
                        if visited[r][c]:
                            continue
                        visited[r][c] = True
                        region.add((r, c))

                        for dr, dc in directions:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < len(board) and 0 <= nc < len(board[row]):
                                if (board[nr][nc] == curr_color) and not visited[nr][nc]:
                                    stack.append((nr, nc))
                    regions.append(region)
        return regions
    

    @staticmethod
    def get_region_liberties(board, region) -> int:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        liberties = 0

        for r, c in region:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(board) and 0 <= nc < len(board[nr]):
                    if board[nr][nc] == [None]:
                        liberties += 1
        return liberties


    @staticmethod
    def delete_region(board, region, player, opponent) -> None:
        for cell in region:
            row, col = cell
            if board[row][col] == player.color:
                player.captures += 1
            else:
                opponent.captures += 1
            board[row][col] = [None]


    @staticmethod
    def manage_regions(board, player, opponent) -> None:
        regions = Go.map_regions(board, player, opponent)

        for region in regions:
            if Go.get_region_liberties(board, region) == 0 and len(regions) > 1:
                Go.delete_region(board, region, player, opponent)

    
    @staticmethod
    def get_empty_cells(board, color) -> List[Tuple[int, int]]:
        moves = []

        for row in range(len(board)):
            for col in range(len(board[row])):
                liberties, same_adj, opposite_adj, sides = Go.get_cell_liberties(board, row, col, color)
                if (board[row][col] == [None] and opposite_adj < sides and (liberties or (same_adj != sides or same_adj >= 2))):
                    moves.append((row, col))
        return moves
    

    @staticmethod
    def get_cell_liberties(board, row, col, color) -> int:
        res, same_adj, opposite_adj, sides = 0, 0, 0, 0
        rows, cols = len(board), len(board[0])
        opposite_color = Go.get_opposite_color(color)

        if row + 1 < rows:
            sides += 1
            if board[row + 1][col] == [None]:
                res += 1
            if board[row + 1][col] == color:
                same_adj += 1
            if board[row + 1][col] == opposite_color:
                opposite_adj += 1

        if row - 1 >= 0:
            sides += 1
            if board[row - 1][col] == [None]:
                res += 1
            if board[row - 1][col] == color:
                same_adj += 1
            if board[row - 1][col] == opposite_color:
                opposite_adj += 1

        if col + 1 < cols:
            sides += 1
            if board[row][col + 1] == [None]:
                res += 1
            if board[row][col + 1] == color:
                same_adj += 1
            if board[row][col + 1] == opposite_color:
                opposite_adj += 1

        if col - 1 >= 0:
            sides += 1
            if board[row][col - 1] == [None]:
                res += 1
            if board[row][col - 1] == color:
                same_adj += 1
            if board[row][col - 1] == opposite_color:
                opposite_adj += 1

        return res, same_adj, opposite_adj, sides

    
    @staticmethod
    def get_opposite_color(color) -> str:
        return "white" if color == "black" else "black"
    

    @staticmethod
    def get_winner(board, player, opponent) -> int:
        if player.color == "white":
            white_captures = player.captures + 6.5
            black_captures = opponent.captures
        else:
            white_captures = opponent.captures + 6.5
            black_captures = player.captures
        
        
        
        for row in board:
            for cell in row:
                if cell == "white":
                    white_captures += 1
                elif cell == "black":
                    black_captures += 1
        
            
        if player.color == "white":
            return 1 if (white_captures > black_captures) else 0
        else:
            return 1 if (white_captures < black_captures) else 0
