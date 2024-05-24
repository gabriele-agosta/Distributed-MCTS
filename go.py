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
    def remove_captured_stones(board, color, color_captured, opponent) -> None:
        visited = [[False for _ in range(len(board))] for _ in range(len(board))]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == color or board[row][col] == color_captured  and not visited[row][col]:
                    stack = [(row, col)]
                    region = set()
                    captured = True

                    while stack:
                        r, c = stack.pop()
                        if visited[r][c]:
                            continue
                        visited[r][c] = True
                        region.add((r, c))

                        for dr, dc in directions:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < len(board) and 0 <= nc < len(board[row]):
                                if board[nr][nc] == [None]:
                                    captured = False
                                elif (board[nr][nc] == color or board[nr][nc] == color_captured)  and not visited[nr][nc]:
                                    stack.append((nr, nc))

                    if captured:
                        for r, c in region:
                            # board[r][c] = Go.white_captured_territory if color == "black" else Go.black_captured_territory
                            board[r][c] = [None]
                            opponent.captures += 1
    
    
    @staticmethod
    def get_empty_cells(board) -> List[Tuple[int, int]]:
        moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == [None] and Go.get_cell_freedom_degrees(board, row, col):
                    moves.append((row, col))
        return moves
    

    @staticmethod
    def get_cell_freedom_degrees(board, row, col) -> int:
        res = 0

        if ( 0 < row + 1 < len(board[row]) ) and (board[row + 1][col] == [None] ):
            res += 1
        if ( 0 < row - 1 < len(board[row]) ) and (board[row - 1][col] == [None] ):
            res += 1
        if ( 0 < col + 1 < len(board[row]) ) and (board[row][col + 1] == [None] ):
            res += 1
        if ( 0 < col - 1 < len(board[row]) ) and (board[row][col - 1] == [None] ):
            res += 1
        return res

    
    @staticmethod
    def get_opposite_color(color) -> str:
        return "white" if color == "black" else "black"
    

    @staticmethod
    def get_winner(board, white, black) -> str:
        white_captures = white.captures + 6.5
        black_captures = black.captures

        for row in board:
            for cell in row:
                if cell == "white" or cell == Go.white_captured_territory:
                    white_captures += 1
                else:
                    black_captures += 1
        
        
        if (white_captures > black_captures):
            return 1
        else:
            return 0
