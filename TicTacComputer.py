# this class should analyze the board position and pick the best move.
class TicTacComputer:
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]

    def __init__(self, board):
        self.board = board
        pass

    def try_win(self):
        #  if there is a winning move, take it
        pass

    def try_block_win(self):
        #  If the opponent is able to win, block their move
        pass

    @staticmethod
    def open_space(self):
        # determine if there is an open space to exploit or defend
        pass


if __name__ == '__main__':
    sample_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    open_win_1 = [[1, 1, 0],
                  [0, 0, 0],
                  [0, 0, 0]]
    open_win_2 = [[1, 0, 0],
                  [0, 0, 0],
                  [1, 0, 0]]
    open_win_3 = [[1, 0, 0],
                  [0, 0, 0],
                  [0, 0, 1]]
