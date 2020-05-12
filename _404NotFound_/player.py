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
        self.round = 0
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
        self.round += 1
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

                explore_area = set()
                for pos, num in self_pieces:
                    for _p in pos.card_neighbour(num):
                        if self.state.get_color(_p.x, _p.y) != color:
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

                ft = self_pieces_num/0.01 if (other_pieces_num == 0) else self_pieces_num/other_pieces_num
                if other_pieces_num - sum(boom_reward) == 0:
                    f0 = (self_pieces_num - sum(boom_penalty)) / 0.01
                else:
                    f0 = (self_pieces_num - sum(boom_penalty)) / (other_pieces_num - sum(boom_reward))
                f2 = len(explore_area)-len(self_pieces)
                f3 = -sum(num*sum(_n*_p.manh_dist(pos) for _p,_n in self_pieces) for pos,num in other_pieces)
                
                # self.state.print()
                # print(self.action, (f0, f1, f2, f3, f4))
                return (ft,f0, f2, f3)
        
        if self.round <= 1:
            if self.color == Color.white:
                return ('MOVE', 1, (3, 0), (3, 1))
            else:
                return ('MOVE', 1, (3, 7), (3, 6))
        else:
            if self.explore_stage():
                return minimax_decision(Minimax_Node(self.board), 1)
            else:
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

    def explore_stage(self):
        color = self.color
        self_pieces = self.board.get_pieces(color)
        other_pieces = self.board.get_pieces(opposite(color))
        for pos, num in self_pieces:
            for _p in pos.card_neighbour(num*2):
                for _op in _p.neighbour():
                    if self.board.get_color(_op.x, _op.y) == opposite(color):
                        return False
        for pos, num in other_pieces:
            for _p in pos.card_neighbour(num*2):
                for _op in _p.neighbour():
                    if self.board.get_color(_op.x, _op.y) == color:
                        return False
        return True
