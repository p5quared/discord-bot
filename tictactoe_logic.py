# making logic for tic-tac-toe game

def computer_opponent():
    choice = input("Battle versus computer? (y/n):\n")
    if choice == "y":
        return True
    return False


class TicTacToe:
    def __init__(self):
        self.board = [[" "] * 3 for _ in range(3)]
        self.curr_turn = "X"
        self.game_over = False
        self.computer = computer_opponent()

    def game_loop(self):
        while not self.game_over:
            target = input(f"Player {self.curr_turn} enter coordinates X Y: ")
            x, y = int(target[0]), 2 - int(target[1])
            if not self.target_is_valid(x, y):
                print("Invalid move, try again...")
                continue
            else:
                self.board[y][x] = self.curr_turn
            print(self)
            if self.win_check():
                continue
            self.curr_turn = "O" if self.curr_turn == "X" else "X"
        print(f'{self.curr_turn} has won!')

    def __str__(self):
        o_string = ""
        o_string += " _" * 3
        o_string += "\n"
        for row in self.board:
            o_string += ("|" + row[0] + "|" + row[1] + "|" + row[2] + "|" + "\n")
        o_string += " -" * 3
        return o_string

    def win_check(self):
        # row success
        for row in self.board:
            if any(item1 == "X" or item1 == "O" for item1 in row):
                if all(item == row[0] for item in row):
                    self.game_over = True
                    return True
        # col success
        cols = [[" "] * 3 for _ in range(3)]
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                cols[j][i] = row[j]
        for col in cols:
            if any(item1 == "X" or item1 == "O" for item1 in col):
                if all(item == col[0] for item in col):
                    self.game_over = True
                    return True
        # diag success
        dia1 = list()
        dia2 = list()
        for i in range(3):
            dia1.append(self.board[i][i])
            dia2.append(self.board[i][2 - i])
        if any(item1 == "X" or item1 == "O" for item1 in dia1):
            if all(item == dia1[0] for item in dia1):
                return True
        if any(item1 == "X" or item1 == "O" for item1 in dia2):
            if all(item == dia2[0] for item in dia2):
                self.game_over = True
                return True
        return False

    def target_is_valid(self, x, y):
        if 2 < x < 0 and 2 < y < 0:
            print("Invalid: Move out of bounds.")
            return False
        if self.board[y][x] != "X" and self.board[y][x] != "Y":
            return True
        else:
            print("Invalid: Space unavailable.")
            return False


if __name__ == "__main__":
    sample_board = TicTacToe()
    print(sample_board)
    sample_board.game_loop()
