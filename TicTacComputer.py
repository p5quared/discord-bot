# this class should analyze the board position and pick the best move.
def tilt_board(board):
    rotated_matrix = [[0 for _ in range(3)] for _ in range(3)]
    for x in range(3):
        for y in range(3):
            rotated_matrix[x][y] = board[2 - y][x]
    return rotated_matrix


def get_diags(board):
    diags = [[0 for _ in range(3)] for _ in range(2)]
    for i in range(3):
        diags[0][i] = board[i][i]
        diags[1][i] = board[i][2 - i]
    print(diags)
    return diags


class TicTacComputer:
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    center = (1, 1)

    def __init__(self, board):  # computer is always 1
        self.board = board
        self.rotated = tilt_board(board)
        self.diag = get_diags(board)

    def try_win(self):
        #  if there is a winning move, take it
        for i, row in enumerate(self.board):
            if row.count(1) == 2:
                return True, (i, row.index(0))
        for i, row in enumerate(self.rotated):
            if row.count(1) == 2:
                return True, (row.index(0), i)
        if self.diag[0].count(1) == 2:
            return True, (self.diag[0].index(0), self.diag[0].index(0))
        if self.diag[1].count(1) == 2:
            return True, (self.diag[1].index(0), 2-self.diag[1].index(0))

    def try_block_win(self):
        #  If the opponent is able to win, block their move
        pass

    @staticmethod
    def open_space(self):
        # determine if there is an open space to exploit or defend
        pass


if __name__ == '__main__':
    sample_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    sample_board_2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    open_win_1 = [[1, 1, 0],
                  [0, 0, 0],
                  [0, 0, 0]]
    open_win_2 = [[1, 0, 0],
                  [0, 0, 0],
                  [1, 0, 0]]
    open_win_3 = [[1, 0, 0],
                  [0, 0, 0],
                  [0, 0, 1]]
    open_win_4 = [[0, 0, 1],
                  [0, 1, 0],
                  [0, 0, 0]]
    # TicTacComputer(sample_board)
    print(TicTacComputer(open_win_1).try_win())
    print(TicTacComputer(open_win_2).try_win())
    print(TicTacComputer(open_win_3).try_win())
    print(TicTacComputer(open_win_4).try_win())
    TicTacComputer(sample_board_2)
