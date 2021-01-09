# Author: Sullivan Lucas Myer
# Date: 12/08/2020
# Description: Sudoku player/verifier/generator

import random
import copy


class Sudoku:
    def __init__(self, board, sud_size):
        """constructs a sudoku board according to user commands"""
        self.puzzle = list(board)
        self.current = [0, 0]
        self.size = sud_size

    def set_cell(self, r, c, v):
        """sets the selected cell to a given value v"""
        self.puzzle[r][c] = v

    def solver(self):
        """Solves puzzle"""
        if self.find_empty() is False:
            return True
        r = self.current[0]  # set row
        c = self.current[1]  # set col
        for n in range(1, (self.size ** 2 + 1)):  # iterate through potential values
            if self.is_valid(r, c, n):  # check temporary viability
                self.set_cell(r, c, n)  # set cell
                if self.solver():  # recurse
                    return True  # declare valid board
            self.puzzle[r][c] = 0  # backtrack
        return False

    def find_empty(self):
        """Finds a cell in need of filling"""
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle)):
                if self.puzzle[i][j] == 0:
                    self.current = [i, j]  # set self.current to an available cell
                    return True
        return False

    def is_valid(self, i, j, value):
        """determines whether placing next value in current cell is valid"""
        if all([value != self.puzzle[i][x] for x in range(self.size ** 2)]):  # check row
            if all([value != self.puzzle[x][j] for x in range(self.size ** 2)]):  # check column
                for x in range(self.size * (i // self.size), self.size * (i // self.size) + self.size):  # check square
                    for y in range(self.size * (j // self.size),
                                   self.size * (j // self.size) + self.size):  # check square
                        if self.puzzle[x][y] == value:  # compare value to cell currently under observation
                            return False
                return True
        return False

    def print_puzzle(self):
        """Prints current state of board"""
        for j in range(1, len(self.puzzle) + 1):
            print(j, end=" ")
            if j % self.size == 0:
                print(" ", end=" ")
        print("")
        for j in range(len(self.puzzle)):
            print("-", end=" ")
            if (j + 1) % self.size == 0:
                print("|", end=" ")
        print("")
        for i in range(len(self.puzzle)):
            if (i + 1) % self.size == 0:
                for ki in range(len(self.puzzle)):
                    print(self.puzzle[i][ki], end=" ")
                    if (ki + 1) % self.size == 0:
                        print("|", end=" ")
                print(i + 1)
                for j in range(len(self.puzzle)):
                    print("-", end=" ")
                    if (j + 1) % self.size == 0:
                        print("|", end=" ")
                print("")
            else:
                for j in range(len(self.puzzle)):
                    print(self.puzzle[i][j], end=' ')
                    if (j + 1) % self.size == 0:
                        print("|", end=" ")
                print(i + 1)

    def better_call_solve(self):
        """Solver Helper"""
        print("Puzzle:")
        self.print_puzzle()
        if self.solver():
            print("Solution:")
            self.print_puzzle()
        else:
            self.print_puzzle()
            print("No solution")

    def verify_puzzle(self):
        """Verifies current state of puzzle is a valid solution"""
        if self.find_empty():
            for i in range(self.size ** 2):
                for j in range(self.size ** 2):
                    self.current = [i, j]
                    n = self.puzzle[i][j]
                    if self.is_valid(i, j, n):
                        continue
                    else:
                        return False
            return True
        else:
            for i in range(self.size ** 2):
                if len(set([self.puzzle[i][x] for x in range(self.size ** 2)])) != 9:  # check rows
                    return False
                elif len(set([self.puzzle[x][i] for x in range(self.size ** 2)])) != 9:
                    return False
                else:
                    upper_left_cell = [((i % self.size) * self.size), ((i // self.size) * self.size)]
                    square = []
                    for x in range(upper_left_cell[0], upper_left_cell[0] + self.size):  # check square
                        for y in range(upper_left_cell[1], upper_left_cell[1] + self.size):  # check square
                            square.append(self.puzzle[x][y])
                    if len(set(square)) != 9:
                        return False
            return True


def engine(puz, s):
    """interface throuhg which user chooses mode"""
    puz_copy = copy.deepcopy(puz)
    sudo = Sudoku(puz, s)
    sudo_c = Sudoku(puz_copy, s)
    game = True
    while game is True:
        sudo.print_puzzle()
        r = -1
        while r not in range(1, 10):
            try:
                r = int(input("Select a row (1-9): "))
            except ValueError:
                print('Invalid Input. Integers only. Please try again.')
        c = -1
        while c not in range(1, 10):
            try:
                c = int(input("Select a column (1-9): "))
            except ValueError:
                print('Invalid Input. Integers only. Please try again.')

        if sudo.puzzle[r - 1][c - 1] != 0:
            if sudo.find_empty():
                print('Cell already filled, please choose another.')
                continue
            else:
                if sudo.verify_puzzle():
                    sudo.print_puzzle()
                    print("YOU WON!")
                    break
                else:
                    sudo.print_puzzle()
                    print("YOU FAILED!")
                    print("Actual Solution:")
                    sudo_c.better_call_solve()
                    break
        num = -1
        while num not in range(1, 10):
            num = input("Enter an integer (1-9) to fill cell,\n"
                        "Q to end game and view solution,\n"
                        "C to check solution and keep playing:\n")
            try:
                num = int(num)
            except ValueError:
                num = num.upper()
                if num == 'Q':
                    sudo_c.better_call_solve()
                    game = False
                    break
                elif num == 'C':
                    if sudo.verify_puzzle():
                        sudo.print_puzzle()
                        print("YOU WON!")
                        break
                    else:
                        print("NOT YET SOLVED")
                else:
                    print('Invalid Input. Please try again.')
        if num == 'Q':
            break
        else:
            sudo.set_cell(r - 1, c - 1, int(num))


if __name__ == '__main__':
    # the following puzzles are starting points for use modes 1 and 2
    puzzles = ([[5, 1, 7, 6, 0, 0, 0, 3, 4],
                [2, 8, 9, 0, 0, 4, 0, 0, 0],
                [3, 4, 6, 2, 0, 5, 0, 9, 0],
                [6, 0, 2, 0, 0, 0, 0, 1, 0],
                [0, 3, 8, 0, 0, 6, 0, 4, 7],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 9, 0, 0, 0, 0, 0, 7, 8],
                [7, 0, 3, 4, 0, 0, 5, 6, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]],

               [[1, 0, 5, 7, 0, 2, 6, 3, 8],
                [2, 0, 0, 0, 0, 6, 0, 0, 5],
                [0, 6, 3, 8, 4, 0, 2, 1, 0],
                [0, 5, 9, 2, 0, 1, 3, 8, 0],
                [0, 0, 2, 0, 5, 8, 0, 0, 9],
                [7, 1, 0, 0, 3, 0, 5, 0, 2],
                [0, 0, 4, 5, 6, 0, 7, 2, 0],
                [5, 0, 0, 0, 0, 4, 0, 6, 3],
                [3, 2, 6, 1, 0, 7, 0, 0, 4]],

               [[8, 5, 0, 0, 0, 2, 4, 0, 0],
                [7, 2, 0, 0, 0, 0, 0, 0, 9],
                [0, 0, 4, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 7, 0, 0, 2],
                [3, 0, 5, 0, 0, 0, 9, 0, 0],
                [0, 4, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 8, 0, 0, 7, 0],
                [0, 1, 7, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 3, 6, 0, 4, 0]],

               [[0, 0, 5, 3, 0, 0, 0, 0, 0],
                [8, 0, 0, 0, 0, 0, 0, 2, 0],
                [0, 7, 0, 0, 1, 0, 5, 0, 0],
                [4, 0, 0, 0, 0, 5, 3, 0, 0],
                [0, 1, 0, 0, 7, 0, 0, 0, 6],
                [0, 0, 3, 2, 0, 0, 0, 8, 0],
                [0, 6, 0, 5, 0, 0, 0, 0, 9],
                [0, 0, 4, 0, 0, 0, 0, 3, 0],
                [0, 0, 0, 0, 0, 9, 7, 0, 0]],

               [[0, 0, 4, 0, 2, 0, 0, 3, 0],
                [5, 0, 0, 4, 0, 0, 0, 0, 0],
                [2, 8, 0, 0, 7, 0, 0, 0, 6],
                [0, 1, 7, 2, 0, 0, 0, 0, 0],
                [0, 9, 0, 1, 5, 6, 0, 4, 0],
                [0, 0, 0, 0, 0, 4, 1, 2, 0],
                [6, 0, 0, 0, 4, 0, 0, 5, 1],
                [0, 0, 0, 0, 0, 5, 0, 0, 8],
                [0, 2, 0, 0, 8, 0, 3, 0, 0]],

               [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                [0, 0, 0, 0, 8, 0, 0, 7, 9]],

               [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                [5, 2, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 7, 0, 0, 0, 0, 3, 1],
                [0, 0, 3, 0, 1, 0, 0, 8, 0],
                [9, 0, 2, 8, 6, 3, 0, 0, 5],
                [0, 5, 0, 0, 9, 0, 6, 0, 0],
                [1, 3, 0, 0, 0, 0, 2, 5, 0],
                [0, 0, 0, 0, 0, 0, 0, 7, 4],
                [0, 0, 5, 2, 0, 6, 3, 0, 0]])

    use_mode = int(input('WELCOME TO CRUDOKU!\n'
                         'a poorly made version of sudoku\n'
                         '\n'
                         '1: Play New Game\n'
                         '2: Auto-Generate Puzzle & Solution\n'
                         '3: Create Your Own Puzzle & Have It Solved\n'))
    while use_mode not in range(4):
        use_mode = int(input('Invalid Input: Please enter one of the options presented above, or 0 to exit.\n'))
    if use_mode == 0:
        print('Until Next Time!')
    elif use_mode == 1:
        engine(puzzles[random.randint(0, 5)], 3)
    elif use_mode == 2:
        Sudoku(puzzles[random.randint(0, 6)], 3).better_call_solve()
    else:
        sudSize = int(input("Please enter game size (3 is standard):\n"))
        print("Enter a " + str(sudSize ** 2) +
              "x" + str(sudSize ** 2) +
              " Sudoku puzzle by typing each cell\n" +
              "separated by a comma, left to right, top to bottom.\n" +
              "Valid numbers: 1-" + str(sudSize ** 2) + " (0' for an empty cell)\n")
        puzzle = []
        for k in range(sudSize ** 2):
            valid_row = True
            while valid_row:
                row = list(map(int, input("Enter row " + str(k + 1) + ": ").split(",")))
                if len(row) == sudSize ** 2:
                    for z in range(sudSize ** 2):
                        if row[z] > sudSize ** 2:
                            valid_row = False
                            break
                        if z > 0:
                            for preceding in range(z):
                                if row[preceding] == row[z] != 0:
                                    valid_row = False
                                    break
                            if valid_row is False:
                                break

                        for p in puzzle:
                            if (row[z] == p[z] != 0) or (row[z] > sudSize ** 2):
                                valid_row = False
                                break
                        if valid_row is False:
                            break
                else:
                    continue
                if valid_row:
                    puzzle.append(row)
                    valid_row = False
                else:
                    valid_row = True
        p = Sudoku(puzzle, sudSize)
        p.better_call_solve()
