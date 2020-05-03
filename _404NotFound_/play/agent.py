"""
The player agent reads the board then make the best move computed by Minimax algorithm
"""

from _404NotFound_.search.board import *
import numpy as np
import csv
import pickle

# import tensorflow as tf
# from tensorflow.compat.v1.nn.rnn_cell import *
# import abc
# from tf_agents.environments import *
# from tf_agents.specs import array_spec
# from tf_agents.trajectories import time_step as ts

class Agent:
    def __init__(self, lr=0.5, use_minimax=0):
        self.lr = lr
        self.use_minimax = use_minimax
        self.colour = Chess.none
        self.history = []
        self.state_values = {}

    def set_colour(self, colour):
        self.colour = colour

    def add_state_value(self, v):
        if v[0] not in self.state_values:
            self.state_values[v[0]] = v[1]

    def eval(self, boom_cells):
        return sum([-1 if cell.chess == self.colour else 1 for cell in boom_cells])

    def move(self, env):
        if self.use_minimax:
            env.board.copy()
        else:
            cells = env.board.get_cells(self.colour)
            boom = []
            for cell in cells:
                boom.append(env.board.get_eval(cell.pos, self.colour))
            if max(boom) > 0:
                point = cells[boom.index(max(boom))].pos
                env.board.set_boom(point)
                return "BOOM", point
            # This simple algorithm only allows pieces to go ahead (since it may be more likely to win)
            while True:
                # _from is a cell while _to is a pos
                _from = random_choose(cells)
                random_num = np.random.choice(_from.num) + 1

                moves = env.board.possible_moves(self.colour)
                _to = random_choose(moves[_from])

                if self.colour == Chess.white:
                    if _from.pos.y < _to.y:
                        continue
                    else:
                        break
                else:
                    if _from.pos.y < _to.y:
                        continue
                    else:
                        break

            env.board.set_move(random_num, _from, env.board.get_p(_to))
            # env.board.print()

            return "MOVE", random_num, (_from.pos.x, _from.pos.y), (_to.x, _to.y)


    def minimax(self, env):
        env.board.possible_moves()

    def update_history(self, action):
        self.history.append(action)

    def reset_history(self):
        self.history = []

    def update(self, env):
        reward = env.reward(self.colour)
        target = reward
        for prev in reversed(self.history):
            # Monte-Carlo learning
            value = self.state_values[prev] + self.lr*(target - self.state_values[prev])
            self.state_values[prev] = value
            target = value
        self.reset_history()




class Environment:
    def __init__(self, board):
        self.board= board
        self.winner = None


    def game_over(self):
        if self.board.is_empty():
            return True
        elif sizeof_cells(self.board.get_white()) == 0:
            self.winner = Chess.black
            return True
        elif sizeof_cells(self.board.get_black()) == 0:
            self.winner = Chess.white
            return True
        else:
            return False


    def reward(self, colour):
        if not self.game_over():
            return 0
        return 1 if self.winner == colour else 0

    def get_state(self):
        # batch_size = [64] # Or [8, 8]
        # state = tf.Variable(tf.zeros_initializer(batch_size), dtype=tf.float32)

        state= [0 for _ in range(64)]
        for cell in self.board.cells:
            if cell.chess == Chess.none:
                state[self.board.pos_dict[cell.pos]] = 0 # 0.5
            elif cell.chess == Chess.white:
                state[self.board.pos_dict[cell.pos]] = cell.num # 0.5 - 1 * cell.num / 24
            else:
                state[self.board.pos_dict[cell.pos]] = 12 + cell.num # 0.5 + 1 * cell.num / 24

        return state


# This function is not used since the expendibot has too many ending states
# It is impossible to generate all of them in a while or in 100MB
def generate_all_possible_winning_states(env, i=0, j=0):
    results = []
    num_stack = [Chess.none] + n_duplicate_elements(Chess.white, 12) + n_duplicate_elements(Chess.black, 12)

    for v in range(len(num_stack)):
        cell = env.board.get_p(Pos(i, j))
        cell.chess = num_stack[v]
        if v != 0:
            cell.num = v - (cell.chess.value-1)*12

        if j == BOARD_LEN-1:
            if i == BOARD_LEN-1:
                if env.board.is_valid():
                    state = env.get_state()
                    ended = env.game_over()
                    results.append((state, env.winner, ended))
            else:
                results += generate_all_possible_winning_states(env, i+1, 0)
        else:
            results += generate_all_possible_winning_states(env, i, j+1)
    return results


class Human:
    def __init__(self, colour):
        self.colour = colour
        self.history= []

    def move(self, env):
        while True:
            try:
                action = input("Enter your action in a tuple (e.g. \"B,11\" || \"10,n,11\"): ")
                action = action.split(",")
                if action[0] == 'B':
                    env.board.set_boom(Pos(int(action[1][0]), int(action[1][1])))
                else:
                    cell = env.board.get_p(Pos(int(action[0][0]), int(action[0][1])))
                    env.board.set_move(int(action[1]), cell, env.board.get_p(Pos(int(action[2][0]), int(action[2][1]))))
                break
            except:
                continue

    def update_history(self, state):
        pass

    def update(self, env):
        pass

    def add_state_value(self, v):
        pass




def play_game(p1, p2, env, plot=False):
    current_player = None

    while not env.game_over():
        current_player = p2 if current_player == p1 else p1

        if plot and ((plot == 1 and current_player == p1) or (plot == 2 and current_player == p2)):
            env.board.print()

        current_player.move(env)
        state = tuple(env.get_state())
        p1.update_history(state)
        p2.update_history(state)

        p1.add_state_value((state, 0.5))
        p2.add_state_value((state, 0.5))
    if plot and ((plot == 1 and current_player == p1) or (plot == 2 and current_player == p2)):
        env.board.print()

    if env.board.is_empty():
        winner = Chess.none
    elif sizeof_cells(env.board.get_white()) > 0:
        winner = Chess.white
    else:
        winner = Chess.black

    p1.add_state_value((p1.history[-1], 1 if winner == p1.colour else -1))
    p2.add_state_value((p2.history[-1], 1 if winner == p2.colour else -1))

    p1.update(env)
    p2.update(env)



def self_train(instance=5000, save_model=1, filename=""):
    p1 = Agent()
    p2 = Agent()

    p1.set_colour(Chess.white)
    p2.set_colour(Chess.black)

    for t in range(instance):
        if t % 500 == 0:
            print(t)
        play_game(p1, p2, Environment(Board()))

    if save_model:
        with open(filename, 'wb') as f:
            pickle.dump([p1, p2], f)


def play_with_human(human_first, agent_name="Agents_N_4000_lr=05.pickle"):
    p1, p2 = pickle.load(open(agent_name, "rb"))
    if human_first:
        human = Human(Chess.white)
        while True:
            play_game(human, p2, Environment(Board()), plot=human_first)
    else:
        human = Human(Chess.black)
        while True:
            play_game(p1, human, Environment(Board()), plot=human_first)





if __name__ == "__main__":
    self_train(100000, save_model=1, filename="Agents_N_100000_lr=05.pickle")

    # play_with_human(1, agent_name="Agents_N_4000_lr=05.pickle")







