from mcst import MCNode, MCEdge
import puzzle
import random as rand
from adi import ADINode


class CreateTrainingSet:
    def __init__(self):
        self.start_state = puzzle.Puzzle()
        self.start_state.board = self.start_state.init_solution()

    # k squares of l walks away from solution
    def create_sets(self, k, l):
        training_sets = []
        for i in range(k):
            puzzle_tree = []
            temp_puzzle = self.start_state
            start_node = self.create_start_node()
            temp_node = start_node
            puzzle_tree.append(temp_node)

            # walks away from solution to
            for j in range(l-1):
                legal_ops = self.get_legal_ops(temp_node)
                random_move = rand.randrange(4)

                while not self.is_legal_move(legal_ops, random_move):
                    random_move = rand.randrange(4)

                if random_move == 0:
                    temp_node.state = temp_puzzle.board.move_up()
                elif random_move == 1:
                    temp_node.state = temp_puzzle.board.move_left()
                elif random_move == 2:
                    temp_node.state = temp_puzzle.board.move_down()
                elif random_move == 3:
                    temp_node.state = temp_puzzle.board.move_right()

                new_node = self.create_adi_node(temp_puzzle.board, temp_node)
                temp_puzzle.board = temp_node.state
                puzzle_tree.append(new_node)

            training_sets.append(puzzle_tree)

        return training_sets

    def generate_training_targets(self, training_sets):
        for data_set in training_sets:
            for sample in data_set:
                self.expand_node(sample)

    @staticmethod
    def create_adi_node(state, parent):
        node = ADINode(state, parent, parent.scrambles + 1)
        node.v = 1
        parent.successors.append(node)
        return node

    def create_start_node(self):
        start_node = ADINode(self.start_state.board)
        start_node.v = 1
        return start_node

    @staticmethod
    def is_legal_move(legal_ops, move):
        if move in legal_ops:
            return True
        return False

    @staticmethod
    def get_legal_ops(node):
        # up == 0
        # left == 1
        # down == 2
        # right == 3
        state = node.state
        colpos = state.player_pos_col
        rowpos = state.player_pos_row
        parent = node.ptr

        legal_ops = []
        moves = {
            0: True,
            1: True,
            2: True,
            3: True
        }

        if node.ptr:
            if colpos < parent.state.player_pos_col:  # moved left, don't right
                moves[3] = False
            elif colpos > parent.state.player_pos_col:  # moved right, don't left
                moves[1] = False
            elif rowpos > parent.state.player_pos_row:  # moved down, don't up
                moves[0] = False
            elif rowpos < parent.state.player_pos_row:  # moved up, don't down
                moves[2] = False

        if colpos > 2:  # On far right col, right illegal
            moves[3] = False
        elif colpos < 1:  # On far left col, left illegal
            moves[1] = False
        if rowpos > 2:  # On bottom row, down illegal
            moves[2] = False
        elif rowpos < 1:  # On top row, up illegal
            moves[0] = False

        for key in moves:
            if moves[key] is True:
                legal_ops.append(key)

        return legal_ops
    
    def expand_node(self, node):
        # up == 0
        # left == 1
        # down == 2
        # right == 3
        if node.successors:
            return
        moves = self.get_legal_ops(node)

        for item in moves:
            new_node = self.create_adi_node(node.state, node)

            if item == 0:
                # print('up')
                new_node.state = new_node.state.move_up()
                new_node.move = 'up'
            elif item == 2:
                # print('down')
                new_node.state = new_node.state.move_down()
                new_node.move = 'down'
            elif item == 1:
                # print('left')
                new_node.state = new_node.state.move_left()
                new_node.move = 'left'
            elif item == 3:
                # print('right')
                new_node.state = new_node.state.move_right()
                new_node.move = 'right'

            node.successors.append(new_node)

    def back_propagate(self, node):
        pass
