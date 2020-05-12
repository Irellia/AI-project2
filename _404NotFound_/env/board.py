"""
The board module represents every entity we will have.
It has 5 classes: Chess, Pos, Cell, Board, BoardNode
"""

import json
from enum import Enum
from functools import reduce

from _404NotFound_.env.pos import *
from _404NotFound_.env.util import *

class Color(Enum):
    none = 0
    white = 1
    black = -1

def opposite(color):
    if color.value < 0:
        return Color.white
    elif color.value > 0:
        return Color.black
    return Color.none

class Board:
    """ constructors """
    # board representation:
    # [<int>*64]
    # =0 for no pieces
    # >0 for white pieces
    # <0 for black pieces
    def __init__(self, reset=False):
        if reset: 
            with open("_404NotFound_/env/init_state.json") as file:
                self.cells = [0 for i in range(BOARD_LEN ** 2)]
                data = json.load(file)
                for stack in data["white"]:
                    self.cells[stack[2] * BOARD_LEN + stack[1]] = stack[0]                    
                for stack in data["black"]:
                    self.cells[stack[2] * BOARD_LEN + stack[1]] = -stack[0]

    def copy(self):
        new = Board()
        new.cells = self.cells.copy()
        return new

    """ query single cell functions """
    def is_blank(self, x, y):
        return self.cells[y * BOARD_LEN +x] == 0

    def is_white(self, x, y):
        return self.cells[y * BOARD_LEN +x] > 0

    def is_black(self, x, y):
        return self.cells[y * BOARD_LEN +x] < 0

    def is_color(self, x, y, color):
        _c = self.cells[y * BOARD_LEN + x]
        return True if _c  * color.value > 0 else _c == color.value

    def get_color(self, x, y):
        if self.is_white(x, y):
            return Color.white
        elif self.is_black(x, y):
            return Color.black
        else:
            return Color.none

    # stack number
    def get_num(self, x, y):
        return abs(self.cells[y * BOARD_LEN +x])

    """ query multiple cells functions """

    # pieces:
    # (<Pos>, <int> - stack number)

    # list of white pieces
    def get_white(self):
        return [(Pos(x, y), self.get_num(x, y)) for x in range(BOARD_LEN) for y in range(BOARD_LEN) if self.is_white(x, y)]

    # list of black pieces
    def get_black(self):
        return [(Pos(x, y), self.get_num(x, y)) for x in range(BOARD_LEN) for y in range(BOARD_LEN) if self.is_black(x, y)]

    # list of pieces with given color
    def get_pieces(self, color):
        return [(Pos(x, y), self.get_num(x, y)) for x in range(BOARD_LEN) for y in range(BOARD_LEN) if self.is_color(x, y, color)]

    # Get the Pos of all pieces that will be influenced by the boom action
    # return [<pieces>]
    def get_boom(self, x, y):
        boom = []
        queue = [Pos(x, y)]
        mark = [False for i in range(BOARD_LEN ** 2)]
        mark[y*BOARD_LEN +x] = True
        while queue:
            pos = queue.pop()
            boom.append((pos, self.get_num(pos.x, pos.y)))
            for neighbour in pos.neighbour():
                if not mark[neighbour.y*BOARD_LEN+neighbour.x]:
                    mark[neighbour.y*BOARD_LEN+neighbour.x] = True
                    if not self.is_blank(neighbour.x, neighbour.y):
                        queue.append(neighbour)
        return boom

    # return {Color.white:[<pieces>], Color.black:[<pieces>]}
    def get_boom_component(self):
        mark = [False for i in range(BOARD_LEN ** 2)]
        boom_component = {Color.white:[], Color.black:[]}
        for x in range(BOARD_LEN):
            for y in range(BOARD_LEN):
                if not mark[y*BOARD_LEN+x] and not self.is_blank(x, y):
                    queue = [Pos(x, y)]
                    mark[y*BOARD_LEN+x] = True
                    black = 0
                    white = 0
                    while queue:
                        pos = queue.pop()
                        if self.get_color(pos.x, pos.y) == Color.white:
                            white += self.get_num(pos.x, pos.y)
                        else:
                            black += self.get_num(pos.x, pos.y)

                        for neighbour in pos.neighbour():
                            if not mark[neighbour.y*BOARD_LEN+neighbour.x]:
                                mark[neighbour.y*BOARD_LEN+neighbour.x] = True
                                if not self.is_blank(neighbour.x, neighbour.y):
                                    queue.append(neighbour)
                    if white > 0 and black > 0:
                        boom_component[Color.white].append(white)
                        boom_component[Color.black].append(black)
        return boom_component


    """ action funcitons
        action representation:
        ("MOVE", n, (xa, ya), (xb, yb)) - move
        ("BOOM", (x, y))                - boom
    """
    # return a new borad state
    # !!! no validation in this fuction
    def apply_action(self, action):
        s = self.copy()
        if action[0] == "MOVE":
            _n = action[1]
            _from = Pos(action[2][0], action[2][1]) 
            _to = Pos(action[3][0], action[3][1])
            _sign = 1 if s.cells[_from.y * BOARD_LEN + _from.x] > 0 else -1
            s.cells[_from.y * BOARD_LEN + _from.x] -= _sign * _n
            s.cells[_to.y * BOARD_LEN + _to.x] += _sign * _n
        elif action[0] == "BOOM":
            for pos, num in s.get_boom(action[1][0], action[1][1]):
                s.cells[pos.y * BOARD_LEN + pos.x] = 0
        return s

    # return a iterable of (<board>, <action>)
    def all_possible_states(self, color):
        pieces = self.get_pieces(color)

        # find possible boom actions
        for pos, num in pieces:
            # ignore entirely friendly fire
            if [1 for _p in pos.neighbour() if self.is_color(_p.x, _p.y, opposite(color))]:
                # generate next state
                a = ("BOOM", (pos.x, pos.y))
                s = self.apply_action(a)
                yield (s, a)
        move_list = []
        for pos, num in pieces:
            # find possible move actions
            for _p in pos.card_neighbour(num):
                # ignore moving onto opposite color pieces
                if self.get_color(_p.x, _p.y) == opposite(color):
                    continue
                # generate next state
                for _n in range(1, num+1):
                    a = ("MOVE", _n, (pos.x, pos.y), (_p.x, _p.y))
                    move_list.append(a)

        map = [0 for i in range(BOARD_LEN**2)]
        for x in range(BOARD_LEN):
             for y in range(BOARD_LEN):
                count = 0
                for neighbour in Pos(x, y).neighbour():
                    if self.get_color(neighbour.x, neighbour.y) == opposite(color):
                        count += 1
                map[y*BOARD_LEN + x] = count

        def _sort_func(action):
            _n = action[1]
            _from = action[2]
            _to = action[3]
            threat = map[_from[0] + _from[1]*BOARD_LEN] - map[_to[0] + _to[1]*BOARD_LEN]
            threat = threat if threat > 0 else 0
            reward = map[_to[0] + _to[1]*BOARD_LEN] - self.get_num(_to[0], _to[1]) - _n
            reward = reward if reward > 0 else 0
            return  - (reward if reward > threat else threat)

        move_list.sort(key = _sort_func)
        for a in move_list:
            s = self.apply_action(a)
            yield (s, a)


    """ print functions """
    def print(self):
        print_dict = {}
        for x in range(BOARD_LEN):
            for y in range(BOARD_LEN):
                num = self.get_num(x, y)
                if self.is_white(x, y):
                    print_dict[(x, y)] = "o" * num if num < 4 else str(num) + "o"
                elif self.is_black(x, y):
                    print_dict[(x, y)] = "x" * num if num < 4 else str(num) + "x"
                else:
                    print_dict[(x, y)] = ""            
        print_board(print_dict, "Board status", True)

