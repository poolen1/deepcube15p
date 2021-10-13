import numpy as np


class AStarNode:
    def __init__(self, state, ptr, g, h):
        self.state = state
        self.ptr = ptr
        self.g = g  # g == depth
        self.h = h  # h == heuristic
        self.f = self.g + self.h
        self.successors = []
        self.move = 'start'


class DFSNode:
    def __init__(self, state, ptr, depth):
        self.state = state
        self.ptr = ptr
        self.d = depth


class AStarSearch:
    def __init__(self, start_state, solution):
        self.start_node = AStarNode(start_state, None, 0, 0)
        self.start_node.h = self.manhattan(self.start_node)
        self.start_node.f = self.start_node.h
        self.end_node = AStarNode(solution, "", 1000, 0)
        self.open_list = []
        self.open_list.append(self.start_node)
        self.closed_list = []
        self.nodes_visited = 0

    def expand_node(self, bestnode):
        if bestnode.successors:
            self.closed_list.append(bestnode)
            return
        moves = self.get_legal_ops(bestnode)

        for item in moves:
            new_node = self.create_successor(bestnode)

            if item == "up":
                # print('up')
                new_node.state = new_node.state.move_up()
                new_node.move = 'up'
            elif item == 'down':
                # print('down')
                new_node.state = new_node.state.move_down()
                new_node.move = 'down'
            elif item == "left":
                # print('left')
                new_node.state = new_node.state.move_left()
                new_node.move = 'left'
            elif item == "right":
                # print('right')
                new_node.state = new_node.state.move_right()
                new_node.move = 'right'

            is_dupe = self.is_dupe(new_node)
            if is_dupe:
                if is_dupe[2] == 'open':
                    old = is_dupe[1]
                    self.open_list.remove(old)
                    if new_node.g > old.g:
                        old.ptr = new_node.ptr
                        new_node = old
                elif is_dupe[2] == 'closed':
                    old = is_dupe[1]
                    self.closed_list.remove(old)
                    if new_node.g > old.g:
                        old.ptr = new_node.ptr
                        new_node = old
                        self.propagate_closed_old(old)

            new_node.h = self.manhattan(new_node)
            new_node.f = new_node.g + new_node.h

            bestnode.successors.append(new_node)

        self.open_list += bestnode.successors

    @staticmethod
    def create_successor(node):
        new_node = AStarNode(node.state, node, node.g + 1, node.h)
        new_node.successors = []
        return new_node

    @staticmethod
    def get_legal_ops(node):
        state = node.state
        colpos = state.player_pos_col
        rowpos = state.player_pos_row
        parent = node.ptr

        legal_ops = []
        moves = {
            'up': True,
            'down': True,
            'left': True,
            'right': True
        }

        if node.ptr:
            if colpos < parent.state.player_pos_col:  # moved left, don't right
                moves['right'] = False
            elif colpos > parent.state.player_pos_col:  # moved right, don't left
                moves['left'] = False
            elif rowpos > parent.state.player_pos_row:  # moved down, don't up
                moves['up'] = False
            elif rowpos < parent.state.player_pos_row:  # moved up, don't down
                moves['down'] = False

        if colpos > 2:  # On far right col, right illegal
            moves['right'] = False
        elif colpos < 1:  # On far left col, left illegal
            moves['left'] = False
        if rowpos > 2:  # On bottom row, down illegal
            moves['down'] = False
        elif rowpos < 1:  # On top row, up illegal
            moves['up'] = False

        for key in moves:
            if moves[key] is True:
                legal_ops.append(key)

        return legal_ops

    def manhattan(self, node):
        solpos = {'1': (0, 0), '2': (0, 1), '3': (0, 2), '4': (0, 3),
                  '5': (1, 0), '6': (1, 1), '7': (1, 2), '8': (1, 3),
                  '9': (2, 0), '10': (2, 1), '11': (2, 2), '12': (2, 3),
                  '13': (3, 0), '14': (3, 1), '15': (3, 2), '0': (3, 3)
                  }
        h = 0
        for col in range(0, 4):
            for row in range(0, 4):
                tile = node.state.board[col][row]
                endpos = solpos[tile]
                solcol = endpos[0]
                solrow = endpos[1]
                h += abs(solcol - col)
                h += abs(solrow - row)
        h *= 10
        return h

    def choose_bestnode(self):
        self.open_list.sort(key=lambda x: x.f, reverse=True)
        bestnode = self.open_list.pop()
        self.closed_list.append(bestnode)

        return bestnode

    def search(self):
        solved = False
        while solved is False:
            if not self.open_list:
                print("Failure")
                exit()

            bestnode = self.choose_bestnode()
            self.nodes_visited += 1

            self.prune(bestnode)

            if bestnode.state.is_solved(self.end_node.state.board):
                path = self.get_path(bestnode)
                solved = True
            else:
                self.expand_node(bestnode)

        # for node in path:
            # print(node.state.board)
        print("Puzzle solved")
        # print("Initial h() value: ", self.start_node.h)
        print("1) Nodes generated: ", self.nodes_visited)
        print("2) Length of path: ", bestnode.g)
        print("3) Path: ")
        # for node in path:
        #     print(node.move, node.state.board)
        return

    def is_dupe(self, node):
        duplicate = False
        for open_node in self.open_list:
            if node.state.board == open_node.state.board:
                duplicate = True
                return duplicate, open_node, 'open'

        for closed_node in self.closed_list:
            if node.state.board == closed_node.state.board:
                duplicate = True
                return duplicate, closed_node, 'closed'
        return duplicate

    @staticmethod
    def propagate_closed_old(old):
        start_node = DFSNode(old, None, 0)
        d_limit = 1000
        open_list = [start_node]
        closed_list = []
        while True:
            if not open_list:
                return
            n = open_list.pop()
            closed_list.append(n)

            if n.d <= d_limit:  # d is less than Depth limit
                if n.state.successors:  # if n has successors
                    for successor in n.state.successors:  # for each successor
                        # if successor points to n, or successor is more expensive,
                        # update new node and continue propagation
                        if successor.ptr == n.state or successor.g < n.state.g:
                            new_node = DFSNode(successor, n, n.d + 1)
                            new_node.state.g = n.state.g + 1
                            new_node.state.f = new_node.state.g + new_node.state.h
                            new_node.state.ptr = n.state
                            open_list.append(new_node)

    def prune(self, bestnode):
        cutoff_value = bestnode.f * 10
        maxf = 0
        for i in range(0, len(self.open_list)):
            node = self.open_list[i]
            if node.f > maxf:
                maxf = node.f
            if node.f >= cutoff_value:
                cutoff_index = i
                del self.open_list[cutoff_index:]
                break

    @staticmethod
    def get_path(final_node):
        the_ptr = final_node.ptr
        the_path = [final_node]
        while the_ptr:
            the_path.append(the_ptr)
            the_ptr = the_ptr.ptr
        the_path.reverse()

        return the_path
