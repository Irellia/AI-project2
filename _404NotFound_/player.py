from functools import reduce

from _404NotFound_.algorithm.minimax import *
from _404NotFound_.env.board import *
from _404NotFound_.env.pos import *


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
        self.color = Color.white if colour == "White" else Color.black
        self.board = Board(True)
        self.board.print()

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
                return not self.state.get_white() or not self.state.get_black()

            def evaluation(self):
                self_pieces = self.state.get_pieces(color)
                other_pieces = self.state.get_pieces(opposite(color))
                self_pieces_num = reduce(lambda x, y: x[1]+y[1], self_pieces)
                other_pieces_num = reduce(lambda x, y: x[1]+y[1], other_pieces)

                explore_area = set()
                for pos, num in self_pieces:
                    for _p in pos.card_neighbour(num):
                        if self.state.get_color(_p.x, _p.y) != opposite(color):
                            explore_area.add(_p)
                
                f0 = self_pieces_num - other_pieces_num
                f1 = 12 - other_pieces_num
                f2 = float(len(explore_area))/64

                return (f0, f1, f2)

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
        self.board.print()
