import copy

from typing import List, Tuple



class Go():
    # Per ora li tengo, eventualmente potrei usarli alla fine per stampare la board aggiornata
    white_captured_territory = "\u2B1C"
    black_captured_territory = "\u2B1B"

    def __init__(self, n) -> None:
        # Potenzialmente potrei creare la board utilizzando un tipo Cell per ogni cella invece di una lista.
        # la cella potrebbe mantenere informazioni sui neighbor, rendendo più facile fare i controlli
        self.board = [[ [None] for _ in range(n) ] for _ in range(n)]
    
    @staticmethod
    def print_board(board) -> None:
        print("\n\n")
        for row in board:
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
    def remove_captured_stones(board, color, color_captured) -> int:
        visited = [[False for _ in range(len(board))] for _ in range(len(board))]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        captured_stones = 0

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
                            board[r][c] = [None]
                            captured_stones += 1
        return captured_stones


    @staticmethod
    def get_empty_cells(board) -> List[Tuple[int, int]]:
        moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == [None] and Go.get_cell_freedom_degrees(board, row, col):
                    moves.append((row, col))
        return moves
    
    
    @staticmethod
    def get_legal_moves(board, color, prev_move) -> List[Tuple[int, int]]:
        moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == [None] and Go.is_legal_move(board, row, col, color, prev_move):
                    moves.append((row, col))
        return moves
    

    @staticmethod
    def is_legal_move(board, row, col, color, prev_move) -> bool:
        temp_board = copy.deepcopy(board)
        temp_board[row][col] = color
        is_loop = prev_move == (row, col)

        captured_stones = Go.remove_captured_stones(temp_board, Go.get_opposite_color(color), None)
        return (Go.get_cell_freedom_degrees(temp_board, row, col) > 0 or captured_stones > 0) and not is_loop


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
    def get_winner(board, color) -> str:
        white, black = 6.5, 0
        empty_cells = [(r, c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] == [None]]
        visited = [[False for _ in range(len(board))] for _ in range(len(board))]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for r, c in empty_cells:
            if not visited[r][c]:
                stack = [(r, c)]
                territory = set()
                borders_white, borders_black = False, False

                while stack:
                    row, col = stack.pop()
                    if visited[row][col]:
                        continue
                    visited[row][col] = True
                    territory.add((row, col))

                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < len(board) and 0 <= nc < len(board[row]):
                            if board[nr][nc] == [None] and not visited[nr][nc]:
                                stack.append((nr, nc))
                            elif board[nr][nc] == "white":
                                borders_white = True
                            elif board[nr][nc] == "black":
                                borders_black = True

                if borders_white and not borders_black:
                    for tr, tc in territory:
                        board[tr][tc] = Go.white_captured_territory
                elif borders_black and not borders_white:
                    for tr, tc in territory:
                        board[tr][tc] = Go.black_captured_territory

        #Go.print_board(board)
        for row in board:
            for cell in row:
                if cell == "white" or cell == Go.white_captured_territory:
                    white += 1
                elif cell == "black" or cell == Go.black_captured_territory:
                    black += 1

        if (white > black and color == "white") or (white < black and color == "black"):
            return 1
        else:
            return 0