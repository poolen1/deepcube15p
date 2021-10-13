from mcst import MCNode


class ADINode:
    def __init__(self, state, ptr=None, scrambles=0):
        self.ptr = ptr
        self.state = state
        self.scrambles = scrambles
        self.v = 0
        self.p = 0
        self.successors = []
