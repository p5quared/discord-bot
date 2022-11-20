class Board:
    def __init__(self):
        self.board = [[0] * 3 for _ in range(3)]

    def rotated_board(self):
        rotated_matrix = [[0 for _ in range(3)] for _ in range(3)]
        for x in range(3):
            for y in range(3):
                rotated_matrix[x][y] = self.board[2 - y][x]
        return rotated_matrix

    def diagonals(self):
        diagonals = [[0 for _ in range(3)] for _ in range(2)]
        for i in range(3):
            diagonals[0][i] = self.board[i][i]
            diagonals[1][i] = self.board[i][2 - i]
        return diagonals