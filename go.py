from typing import List, Tuple


class Go():
    white_captured_territory = "\u2B1C"
    black_captured_territory = "\u2B1B"

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
                    curr_territory = Go.white_captured_territory if curr_color == "White" else Go.black_captured_territory
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
                                if board[nr][nc] == curr_color or board[nr][nc] == curr_territory and not visited[nr][nc]:
                                    stack.append((nr, nc))
                    regions.append(region)
        return regions
    

    @staticmethod
    def get_region_liberties(board, region) -> int:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        liberties = 0

        for r, c in region:
            territory = [None]
            if board[r][c] == "black":
                territory = Go.black_captured_territory 
            elif board[r][c] == "white":
                territory = Go.white_captured_territory 

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(board) and 0 <= nc < len(board[nr]):
                    if board[nr][nc] == [None] or board[nr][nc] == territory:
                        liberties += 1
        return liberties


    @staticmethod
    def delete_region(board, region, player, opponent) -> None:
        for cell in region:
            row, col = cell
            if board[row][col] == opponent.color:
                player.captures += 1
            else:
                opponent.captures += 1
            if board[row][col] == "white" or board[row][col] == Go.white_captured_territory: 
                board[row][col] = Go.black_captured_territory 
            elif board[row][col] == "black" or board[row][col] == Go.black_captured_territory: 
                board[row][col] = Go.white_captured_territory 


    @staticmethod
    def manage_regions(board, player, opponent) -> None:
        regions = Go.map_regions(board, player, opponent)

        if len(regions) > 2:
            for region in regions:
                if Go.get_region_liberties(board, region) == 0:
                    Go.delete_region(board, region, player, opponent)

        elif len(regions) == 2 and not Go.get_empty_cells(board, player.color) and not Go.get_empty_cells(board, opponent.color):
            captured_region = regions[0] if len(regions[0]) < len(regions[1]) else regions[1]
            Go.delete_region(board, captured_region, player, opponent)

    
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
        acceptable = [[None]]

        if row + 1 < rows:
            sides += 1
            if board[row + 1][col] in acceptable:
                res += 1
            if board[row + 1][col] == color:
                same_adj += 1
            if board[row + 1][col] == opposite_color:
                opposite_adj += 1

        if row - 1 >= 0:
            sides += 1
            if board[row - 1][col] in acceptable:
                res += 1
            if board[row - 1][col] == color:
                same_adj += 1
            if board[row - 1][col] == opposite_color:
                opposite_adj += 1

        if col + 1 < cols:
            sides += 1
            if board[row][col + 1] in acceptable:
                res += 1
            if board[row][col + 1] == color:
                same_adj += 1
            if board[row][col + 1] == opposite_color:
                opposite_adj += 1

        if col - 1 >= 0:
            sides += 1
            if board[row][col - 1] in acceptable:
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
                if cell == Go.white_captured_territory:
                    white_captures += 1
                elif cell == Go.black_captured_territory:
                    black_captures += 1
        
            
        if player.color == "white":
            return 1 if (white_captures > black_captures) else 0
        else:
            return 0 if (white_captures < black_captures) else 1
