# making logic for tic-tac-toe game

def computer_opponent():
    choice = input("Battle versus computer? (y/n):\n")
    if choice == "y":
        return True
    return False


def rotated_board(board):
    rotated_matrix = [[0 for _ in range(3)] for _ in range(3)]
    for x in range(3):
        for y in range(3):
            rotated_matrix[x][y] = board[2 - y][x]
    return rotated_matrix


class TicTacToe:
    def __init__(self):
        self.board = [[0] * 3 for _ in range(3)]
        self.curr_turn = 1
        self.game_over = False
        self.computer = computer_opponent()

    def game_loop(self):
        while not self.game_over:
            x, y = self.get_player_move()
            self.board[y][x] = self.curr_turn
            print(self)
            if self.win_check():
                continue
            self.curr_turn = 2 if self.curr_turn == 1 else 1
        print(f'{"X" if self.curr_turn == 1 else "O"} has won!')

    def get_player_move(self):
        while True:
            target = input(f"Player {self.curr_turn} enter coordinates X Y: ")
            x, y = int(target[0]), 2-int(target[1])
            if self.target_is_valid(x, y):
                break
        return x, y

    def __str__(self):
        o_string = ""
        o_string += " _" * 3
        o_string += "\n"
        pretty_board = [[""] * 3 for _ in range(3)]
        for i, row in enumerate(self.board):
            print(f'({i}, {row}')
            for j, item in enumerate(row):
                if item == 0:
                    pretty_board[i][j] = " "
                if item == 1:
                    pretty_board[i][j] = "X"
                if item == 2:
                    pretty_board[i][j] = "O"

        print(pretty_board)
        for row in pretty_board:
            o_string += ("|" + row[0] + "|" + row[1] + "|" + row[2] + "|" + "\n")
        o_string += " -" * 3
        return o_string

    def win_check(self):
        # row success
        for row in self.board:
            print(row)
            if any(item1 == 1 or item1 == 2 for item1 in row):
                if all(item == row[0] for item in row):
                    self.game_over = True
                    return True
        # col success
        cols = rotated_board(self.board)
        for col in cols:
            if any(item1 == 1 or item1 == 2 for item1 in col):
                if all(item == col[0] for item in col):
                    self.game_over = True
                    return True

        # diag success
        dia1 = list()
        dia2 = list()
        for i in range(3):
            dia1.append(self.board[i][i])
            dia2.append(self.board[i][2 - i])
        if any(item1 == 1 or item1 == 2 for item1 in dia1):
            if all(item == dia1[0] for item in dia1):
                return True
        if any(item1 == 1 or item1 == 2 for item1 in dia2):
            if all(item == dia2[0] for item in dia2):
                self.game_over = True
                return True
        return False

    def target_is_valid(self, x, y):
        if 2 < x < 0 and 2 < y < 0:
            print("Invalid: Move out of bounds.")
            return False
        if self.board[y][x] == 0:
            return True
        else:
            print("Invalid: Space unavailable.")
            return False


if __name__ == "__main__":
    sample_board = TicTacToe()
    print(sample_board)
    sample_board.game_loop()
