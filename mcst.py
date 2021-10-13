import random as rand
import math
import copy


class MCEdge:
    def __init__(self):
        self.count = 0     # Number of times action a taken from state s
        self.max_val = 0    # Maximal value of action a from state s
        self.cvl = 0    # Current Virtual Loss
        self.prior = 0  # Prior probability of action a from state s


class MCNode:
    def __init__(self, state, ptr=None, move=None):
        self.state = state
        self.ptr = ptr
        self.move = move
        self.wins = 0
        self.sims = 0
        self.successors = []


class mcst:
    def __init__(self, start_state, solution):
        self.start_node = MCNode(start_state)
