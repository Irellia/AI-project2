"""
This module contains some helper functions for printing actions and boards.
Feel free to use and/or modify them to help you develop your program.
"""

import numpy as np

def random_choose(data):
    return data[np.random.choice(len(data))]

def sizeof_cells(cells):
    return sum([cell.num for cell in cells])

def sizeof_dict(dictionary):
    size = 0
    for i in dictionary:
        size += len(dictionary[i])
    return size

def n_duplicate_elements(element, n):
    return [element for _ in range(n)]


# For debug
# def print_moves(move_dict):
#     for i in move_dict:
#         print(i.pos, i.num, [(j.x, j.y) for j in move_dict[i]])

def print_actions(action_arr):
    for i in action_arr:
        if type(i) == tuple:
            print("Move", i[1], i[0], i[2])
        else:
            print("BOOM", i)

def return_apply_action(action, env):
    if type(action) == tuple:
        env.board.set_move(action[0], env.board.get_p(action[1]), env.board.get_p(action[2]))
        return "Move", action[1], action[0], action[2]
    env.board.set_boom(action)
    return "BOOM", action


def print_move(n, x_a, y_a, x_b, y_b, **kwargs):
    """
    Output a move action of n pieces from square (x_a, y_a)
    to square (x_b, y_b), according to the format instructions.
    """
    print("MOVE {} from {} to {}.".format(n, (x_a, y_a), (x_b, y_b)), **kwargs)


def print_boom(x, y, **kwargs):
    """
    Output a boom action initiated at square (x, y) according to
    the format instructions.
    """
    print("BOOM at {}.".format((x, y)), **kwargs)


def print_board(board_dict, message="", unicode=False, compact=True, **kwargs):
    """
    For help with visualisation and debugging: output a board diagram with
    any information you like (tokens, heuristic values, distances, etc.).

    Arguments:
    board_dict -- A dictionary with (x, y) tuples as keys (x, y in range(8))
        and printable objects (e.g. strings, numbers) as values. This function
        will arrange these printable values on the grid and output the result.
        Note: At most the first 3 characters will be printed from the string
        representation of each value.
    message -- A printable object (e.g. string, number) that will be placed
        above the board in the visualisation. Default is "" (no message).
    unicode -- True if you want to use non-ASCII symbols in the board
        visualisation (see below), False to use only ASCII symbols.
        Default is False, since the unicode symbols may not agree with some
        terminal emulators.
    compact -- True if you want to use a compact board visualisation, with
        coordinates along the edges of the board, False to use a bigger one
        with coordinates alongside the printable information in each square.
        Default True (small board).
    
    Any other keyword arguments are passed through to the print function.
    """
    if unicode:
        if compact:
            template = """# {}
#    ┌───┬───┬───┬───┬───┬───┬───┬───┐
#  7 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  6 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  5 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  4 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  3 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  2 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  1 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  0 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    └───┴───┴───┴───┴───┴───┴───┴───┘
# y/x  0   1   2   3   4   5   6   7"""
        else:
            template = """# {}
# ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,7 │ 1,7 │ 2,7 │ 3,7 │ 4,7 │ 5,7 │ 6,7 │ 7,7 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,6 │ 1,6 │ 2,6 │ 3,6 │ 4,6 │ 5,6 │ 6,6 │ 7,6 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,5 │ 1,5 │ 2,5 │ 3,5 │ 4,5 │ 5,5 │ 6,5 │ 7,5 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,4 │ 1,4 │ 2,4 │ 3,4 │ 4,4 │ 5,4 │ 6,4 │ 7,4 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,3 │ 1,3 │ 2,3 │ 3,3 │ 4,3 │ 5,3 │ 6,3 │ 7,3 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,2 │ 1,2 │ 2,2 │ 3,2 │ 4,2 │ 5,2 │ 6,2 │ 7,2 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,1 │ 1,1 │ 2,1 │ 3,1 │ 4,1 │ 5,1 │ 6,1 │ 7,1 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,0 │ 1,0 │ 2,0 │ 3,0 │ 4,0 │ 5,0 │ 6,0 │ 7,0 │
# └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘"""
    else:
        if compact:
            template = """# {}
#    +---+---+---+---+---+---+---+---+
#  7 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  6 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  5 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  4 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  3 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  2 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  1 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  0 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
# y/x  0   1   2   3   4   5   6   7"""
        else:
            template = """# {}
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,7 | 1,7 | 2,7 | 3,7 | 4,7 | 5,7 | 6,7 | 7,7 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,6 | 1,6 | 2,6 | 3,6 | 4,6 | 5,6 | 6,6 | 7,6 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,5 | 1,5 | 2,5 | 3,5 | 4,5 | 5,5 | 6,5 | 7,5 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,4 | 1,4 | 2,4 | 3,4 | 4,4 | 5,4 | 6,4 | 7,4 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,3 | 1,3 | 2,3 | 3,3 | 4,3 | 5,3 | 6,3 | 7,3 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,2 | 1,2 | 2,2 | 3,2 | 4,2 | 5,2 | 6,2 | 7,2 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,1 | 1,1 | 2,1 | 3,1 | 4,1 | 5,1 | 6,1 | 7,1 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,0 | 1,0 | 2,0 | 3,0 | 4,0 | 5,0 | 6,0 | 7,0 |
# +-----+-----+-----+-----+-----+-----+-----+-----+"""
    # board the board string
    coords = [(x,7-y) for y in range(8) for x in range(8)]
    cells = []
    for xy in coords:
        if xy not in board_dict:
            cells.append("   ")
        else:
            cells.append(str(board_dict[xy])[:3].center(3))
    # print it
    print(template.format(message, *cells), **kwargs)


def expand_nodes(path):
    return [i[0] for i in path for j in range(i[1])]


# Output the result as required
def get_output(path, target):
    current = expand_nodes(path[0].white)
    for i in range(1, len(path)):
        next_path = expand_nodes(path[i].white)
        diff = setdiff(current, next_path)
        print_move(diff[0], diff[1].x, diff[1].y, diff[2].x, diff[2].y)
        current = expand_nodes(path[i].white)
    print_boom(target.x, target.y)


# set difference between two lists, return the length of how many different items between the two lists.
# This function will be used to extract the path in AStar search. Each path only only one stack.
# So just need to return the first item of the remaining element in list1 and list2 wil give the "from" and "to"
def setdiff(lst1, lst2):
    lst1_copy = [i for i in lst1]
    lst2_copy = [i for i in lst2]
    for i in lst1:
        if i in lst2_copy:
            lst1_copy.remove(i)
            lst2_copy.remove(i)
    return len(lst1_copy), lst1_copy[0], lst2_copy[0]

