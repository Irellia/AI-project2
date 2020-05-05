BOARD_LEN = 8

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

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Pos(self.x * other, self.y * other)

    def __floordiv__(self, other):
        return Pos(self.x // other, self.y // other)

    def __truediv__(self, other):
        return Pos(self.x / other, self.y / other)

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
