from enum import Enum


class MMStage(Enum):
    min_stage = 0
    max_stage = 1


class Node:
    def __init__(self, state, action=None):
        self.state = state
        self.action = action

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
    res = None
    res_node = None
    a = None
    for node in init_node.successors(MMStage.max_stage):
        node_value, leaf = minimax_min(node, a, None, depth-1)
        if not a or node_value > a:
            a = node_value
            res = node.action
            res_node = leaf
    res_node.state.print()
    print(res_node.action)
    return res


def minimax_max(node, a, b, depth):
    if depth == 0 or node.cutoff():
        return node.evaluation(), node
    res_node = None
    for successor in node.successors(MMStage.max_stage):
        #print(successor.action)
        min_value, leaf = minimax_min(successor, a, b, depth-1)
        if not a or min_value > a:
            a = min_value
            res_node = leaf
        if b and a >= b:
            return b, res_node
    return a, res_node


def minimax_min(node, a, b, depth):
    if depth == 0 or node.cutoff():
        return node.evaluation(), node
    res_node = None
    for successor in node.successors(MMStage.min_stage):
        #print(successor.action)
        max_value,leaf = minimax_max(successor, a, b, depth-1)
        if not b or max_value < b:
            b = max_value
            res_node = leaf
        if a and b <= a:
            return a, res_node
    return b, res_node
