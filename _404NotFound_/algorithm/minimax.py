from enum import Enum


class MMStage(Enum):
    min_stage = 0
    max_stage = 1

class Node:
    def __init__(self, state, action=None):
        self.state = state
        self.acion = action

    # return a iterable of successor nodes
    def successors(self, minimax_stage):
        pass

    # return boolean corresponding to the ending condition
    def cutoff(self):
        pass

    # return a comparable value
    def evaluation(self):
        pass

    def __lt__(self, other):
        return self.evaluation() < other.evaluation()

def minimax_decision(init_node, depth):
    max_action = None
    max_value = None
    first = True
    for node in init_node.successors(MMStage.max_stage):
        node_value = minimax_max(node, None, None, depth-1)
        if first or node_value > max_value:
            first = False
            max_value = node_value
            max_action = node.action
    return max_action

def minimax_max(node, a, b, depth):
    if depth == 0 or node.cutoff():
        return node.evaluation()
    for successor in node.successors(MMStage.max_stage):
        min_value = minimax_min(successor, a, b, depth-1)
        a = max(a, min_value) if a else min_value
        if b and a >= b:
            return b
    return a


def minimax_min(node, a, b, depth):
    if depth == 0 or node.cutoff():
        return node.evaluation()
    for successor in node.successors(MMStage.min_stage):
        max_value = minimax_max(successor, a, b, depth-1)
        b = min(a, max_value) if b else max_value
        if a and b <= a:
            return a
    return b


