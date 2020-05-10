from _404NotFound_.algorithm.minimax import *
from _404NotFound_.env.board import *
from _404NotFound_.env.pos import *

from functools import reduce

class Player:

    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        """
        self.color = Color.white if colour == "white" else Color.black
        self.board = Board(True)

    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        color = self.color
        class Minimax_Node(Node):

            def __init__(self, board, action=None):
                super().__init__(board, action)

            def successors(self, minimax_stage):
                if minimax_stage == MMStage.max_stage:
                    for board, action in self.state.all_possible_states(color):
                        yield Minimax_Node(board, action)
                else:
                    for board, action in self.state.all_possible_states(opposite(color)):
                        yield Minimax_Node(board, action)

            def cutoff(self):
                return not self.state.get_black() or not self.state.get_white()

            def evaluation(self):
                self_pieces = self.state.get_pieces(color)
                other_pieces = self.state.get_pieces(opposite(color))

                self_pieces_num = sum(stack[1] for stack in self_pieces)
                other_pieces_num = sum(stack[1] for stack in other_pieces)

                self_pieces_centroid = reduce(lambda x, y: x+y, (stack[0] for stack in self_pieces))/self_pieces_num if self_pieces else Pos(3.5, 3.5)
                other_pieces_centroid = reduce(lambda x, y: x+y, (stack[0] for stack in other_pieces))/other_pieces_num if other_pieces else Pos(3.5, 3.5)                

                explore_area = set()
                for pos, num in self_pieces:
                    for _p in pos.card_neighbour(num):
                        if self.state.get_color(_p.x, _p.y) == Color.none:
                            explore_area.add(_p)

                boom_component = self.state.get_boom_component()
                boom_reward = []
                boom_penalty = []
                for i in range(len(boom_component[Color.white])):
                    delta = self_pieces_num/other_pieces_num * boom_component[opposite(color)][i] - boom_component[color][i]
                    if delta > 0:
                        boom_reward.append(delta)
                    else:
                        boom_penalty.append(-delta)
                if not other_pieces_num:
                    f0 = 999
                else:
                    f0 = self_pieces_num + (max(boom_reward) if boom_reward else 0) - \
                    other_pieces_num - (max(boom_penalty) if boom_penalty else 0)
                f1 = sum(boom_reward) - sum(boom_penalty)
                f2 = len(explore_area)
                f3 = -self_pieces_centroid.manh_dist(other_pieces_centroid)
                
                # self.state.print()
                # print(self.action, (f0, f1, f2, f3, f4))
                return (f0, f1, f2, f3)


        return minimax_decision(Minimax_Node(self.board), 3)


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        self.board = self.board.apply_action(action)
