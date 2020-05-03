"""
The board module represents every entity we will have.
It has 5 classes: Chess, Pos, Cell, Board, BoardNode
"""

import json
from enum import Enum
from collections import defaultdict

from _404NotFound_.search.util import *
from _404NotFound_.algorithm.AStarSearch import *

BOARD_LEN = 8


class Chess(Enum):
    none = 0
    white = 1
    black = 2


class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def off_board(self):
        return self.x < 0 or self.x >= BOARD_LEN or self.y < 0 or self.y >= BOARD_LEN

    def neighbour(self):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new = Pos(self.x + dx, self.y + dy)
                if (not (new == self or new.off_board())):
                    yield new

    def card_neighbour(self, distance):
        for dx in range(-distance, distance + 1):
            new_x = self.x + dx
            if (dx != 0 and new_x >= 0 and new_x < BOARD_LEN):
                yield Pos(new_x, self.y)

        for dy in range(-distance, distance + 1):
            new_y = self.y + dy
            if (dy != 0 and new_y >= 0 and new_y < BOARD_LEN):
                yield Pos(self.x, new_y)

    def manh_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        else:
            return False

    def __hash__(self):
        return self.x + self.y * BOARD_LEN

    def __str__(self):
        return str((self.x, self.y))


# A cell contains the position, how many white/blacks on it and the zone number it is in
class Cell:

    def __init__(self, x, y):
        self.pos = Pos(x, y)
        self.chess = Chess.none
        self.num = 0
        self.zone = 0
    
    def copy(self):
        new = Cell(self.pos.x, self.pos.y)
        new.chess = self.chess
        new.num = self.num
        new.zone = self.zone
        return new


class Board:

    def __init__(self):
        self.cells = []
        self.new_board()
        self.pos_dict = {}
        self.new_pos_dict()

    # Preprocess the data provided and parse it into Board
    def new_board(self):
        self.cells = [Cell(i % BOARD_LEN, i // BOARD_LEN) for i in range(BOARD_LEN ** 2)]
        with open("../init_state.json") as file:
            data = json.load(file)
        for pieces in data["white"]:
            self.get(pieces[1], pieces[2]).num = pieces[0]
            self.get(pieces[1], pieces[2]).chess = Chess.white
        for pieces in data["black"]:
            self.get(pieces[1], pieces[2]).num = pieces[0]
            self.get(pieces[1], pieces[2]).chess = Chess.black
        self.__update_zone()

    def new_pos_dict(self):
        idx = 0
        for cell in self.cells:
            self.pos_dict[cell.pos] = idx
            idx += 1


    def is_empty(self):
        for cell in self.cells:
            if cell.chess != Chess.none:
                return False
        return True

    def is_valid(self):
        if sizeof_cells(self.get_my_cells()) > 12 or sizeof_cells(self.get_opp_cells()) > 12:
            return False
        return True

    def copy(self):
        new = Board()
        new.cells = [cell.copy() for cell in self.cells]
        return new

    def get(self, x, y):
        return self.cells[y * BOARD_LEN + x]

    def get_p(self, pos):
        return self.cells[pos.y * BOARD_LEN + pos.x]

    def get_white(self):
        return [cell for cell in self.cells if cell.chess == Chess.white]

    def get_black(self):
        return [cell for cell in self.cells if cell.chess == Chess.black]

    def get_cells(self, colour):
        return [cell for cell in self.cells if cell.chess == colour]

    # Find the cells that each my cell can reach
    def possible_moves(self, colour):
        moves = defaultdict()
        cells = self.get_white() if colour == Chess.white else self.get_black()
        for cell in cells:
            moves[cell] = []
            for neighbour in cell.pos.card_neighbour(cell.num):
                moves[cell].append(neighbour)
        return moves

    # # For debug
    # def print_possible_moves(self):
    #     p_m = self.possible_moves()
    #     for i in p_m:
    #         print(i.pos, i.num, [(j.x, j.y) for j in p_m[i]])

    # def eval(self):
    #     return sizeof_cells(self.get_my_cells()) - sizeof_cells(self.get_opp_cells())

    # Get all points that will be influenced by the boom action
    def get_boom(self, start):
        mark = defaultdict(bool)
        queue = [start]
        boom = set()
        boom.add(start)
        while queue:
            pos = queue.pop()
            mark[pos] = True
            for neighbour in Pos(pos.x, pos.y).neighbour():
                if not mark[neighbour]:
                    if self.get_p(neighbour).chess != Chess.none:
                        queue.append(neighbour)
                    boom.add(neighbour)
        return boom

    def set_white(self, white):
        for cell in self.cells:
            if cell.chess == Chess.white:
                cell.num = 0
                cell.chess = Chess.none
        for pos, num in white:
            cell = self.get_p(pos)
            cell.num = num
            cell.chess = Chess.white

    def get_eval(self, target, colour):
        boom = self.get_boom(target)
        delta = 0
        for pos in boom:
            if self.get_p(pos).chess == colour:
                delta -= 1
            elif self.get_p(pos).chess != Chess.none:
                delta += 1
        return delta


    def set_boom(self, target):
        boom = self.get_boom(target)
        for pos in boom:
            cell = self.get_p(pos)
            cell.num = 0
            cell.chess = Chess.none
        self.__update_zone()

    def set_move(self, n, _from, _to):
        _from.num -= n
        _to.num += n

        _to.chess = _from.chess
        if _from.num == 0:
            _from.chess = Chess.none
        self.__update_zone()


    # Helper function to print the board
    def print(self):
        print_dict = {}
        for cell in self.cells:
            if cell.chess == Chess.black:
                print_dict[(cell.pos.x, cell.pos.y)] = "x" * cell.num
            elif cell.chess == Chess.white:
                print_dict[(cell.pos.x, cell.pos.y)] = "o" * cell.num
            else:
                print_dict[(cell.pos.x, cell.pos.y)] = ""
        print_board(print_dict, "Board status", True)

    # Helper function to show the zone
    def print_zone(self):
        print_dict = {}
        for cell in self.cells:
            if cell.chess == Chess.black:
                print_dict[(cell.pos.x, cell.pos.y)] = "x"
            elif cell.chess == Chess.white:
                print_dict[(cell.pos.x, cell.pos.y)] = "o " + str(cell.zone)
            else:
                print_dict[(cell.pos.x, cell.pos.y)] = cell.zone
        print_board(print_dict, "Board zone status", True)

    # Update the zone occupies after every changes
    def __update_zone(self):
        zone = 1
        mark = defaultdict(bool)
        queue = []

        for x in range(BOARD_LEN):
            for y in range(BOARD_LEN):
                start = Pos(x, y)
                if (mark[start] or self.get_p(start).chess == Chess.black):
                    continue

                queue.append(start)
                while queue:
                    pos = queue.pop()
                    mark[pos] = True

                    self.get_p(pos).zone = zone

                    for neighbour in Pos(pos.x, pos.y).card_neighbour(1):
                        if not mark[neighbour] and self.get_p(neighbour).chess != Chess.black:
                            queue.append(neighbour)

                zone += 1




