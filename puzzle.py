import numpy as np
import copy
import random as rand


class Puzzle:
    def __init__(self, file=None, g=None):
        self.rows = 4
        self.cols = 4
        self.board = []
        self.solution = []
        self.player_pos_col = 0
        self.player_pos_row = 0

        if g is None:
            self.g = 0
        else:
            self.g = g + 1

        if self.g == 0:
            solvable = False
            while not solvable:
                self.init_board(file)
                # Get player pos
                self.player_pos_row, self.player_pos_col = \
                    self.get_player_position(self)
                # Check for solvability
                solvable = self.is_solvable()
                if file is not None and solvable is False:
                    print('exiting')
                    exit()

    def init_board(self, file):
        # Set up board randomly
        self.board = []
        if file is None:
            n = np.random.choice(range(16), 16, replace=False)
            i = 0
            for col in range(self.cols):
                board_row = []
                for row in range(self.rows):
                    board_row.append(str(n[i]))
                    i += 1
                self.board.append(board_row)
        # Set up board with file
        else:
            for line in file.readlines():
                self.board.append(line.split())

    def init_solution(self):
        # Get solution
        solution = copy.deepcopy(self)
        board = []
        i = 1
        for col in range(self.cols):
            solution_row = []
            for row in range(self.rows):
                solution_row.append(str(i))
                i += 1
            board.append(solution_row)
        board[3][3] = '0'
        solution.board = board
        solution.player_pos_row, solution.player_pos_col = \
            self.get_player_position(solution)
        return solution

    def get_player_position(self, board):
        for col in range(self.cols):
            for row in range(self.rows):
                if board.board[col][row] == '0':
                    pos_row = col
                    pos_col = row
                    return pos_row, pos_col

    def is_solvable(self):
        solvable = False
        inv_count = self.count_inversions()
        if self.player_pos_row % 2 == 0:  # Empty pos is on even row
            # odd number of inversions
            if inv_count % 2 == 1:
                solvable = True
        else:  # Empty pos is on odd row
            # even number of inversions
            if inv_count % 2 == 0:
                solvable = True
        return solvable

    def count_inversions(self):
        inv_count = 0
        arr = []
        for idn, n in np.ndenumerate(self.board):
            arr.append(n.astype(np.int))
        for i in range(len(arr)):
            if arr[i] == 0:
                continue
            for j in range(i + 1, 16):
                if arr[j].astype(np.int) == 0:
                    continue
                if arr[i] > arr[j]:
                    inv_count += 1
        return inv_count

    def is_solved(self, solution):
        if self.board == solution:
            return True
        else:
            return False

    def move_up(self):
        posrow = self.player_pos_row
        poscol = self.player_pos_col

        p_node = copy.deepcopy(self)
        p_node.board[posrow][poscol], p_node.board[posrow - 1][poscol]\
            = p_node.board[posrow - 1][poscol], p_node.board[posrow][poscol]
        p_node.player_pos_row, p_node.player_pos_col \
            = p_node.get_player_position(p_node)

        return p_node

    def move_down(self):
        posrow = self.player_pos_row
        poscol = self.player_pos_col

        p_node = copy.deepcopy(self)

        p_node.board[posrow][poscol], p_node.board[posrow + 1][poscol] \
            = p_node.board[posrow + 1][poscol], p_node.board[posrow][poscol]
        p_node.player_pos_row, p_node.player_pos_col \
            = p_node.get_player_position(p_node)

        return p_node

    def move_left(self):
        posrow = self.player_pos_row
        poscol = self.player_pos_col

        p_node = copy.deepcopy(self)
        p_node.board[posrow][poscol], p_node.board[posrow][poscol - 1] \
            = p_node.board[posrow][poscol - 1], p_node.board[posrow][poscol]
        p_node.player_pos_row, p_node.player_pos_col \
            = p_node.get_player_position(p_node)

        return p_node

    def move_right(self):
        posrow = self.player_pos_row
        poscol = self.player_pos_col

        p_node = copy.deepcopy(self)
        p_node.board[posrow][poscol], p_node.board[posrow][poscol + 1] \
            = p_node.board[posrow][poscol + 1], p_node.board[posrow][poscol]
        p_node.player_pos_row, p_node.player_pos_col \
            = p_node.get_player_position(p_node)

        return p_node

