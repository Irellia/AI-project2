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
        self.board.print()
        example = "'m 1 2 4 3 5 ' - (MOVE, 1, (2, 3), (4, 5))\n'b 1 2' - (BOOM, (1, 2))\n"
        string = input("input your action:\n" + example)
        action = self.parse_action(string)
        if action and self.validate_action(action):
            return action
        else:
            while True:
                string = input("Invalid move!! try again:\n")
                action = self.parse_action(string)
                if action and self.validate_action(action):
                    return action



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

    def parse_action(self, string):       
        try:
            inputs = string.split()
            if inputs[0].lower() == 'm' or inputs[0].lower == 'move':
                return ("MOVE", int(inputs[1]), (int(inputs[2]), int(inputs[3])), (int(inputs[4]), int(inputs[5])))
            elif inputs[0].lower() == 'b' or inputs[0].lower == 'boom':
                return ("BOOM", (int(inputs[1]), int(inputs[2])))
        except:
            return None


    def validate_action(self, action):
        if action[0] == "MOVE":
            _n = action[1]
            _from = Pos(action[2][0], action[2][1])
            _to = Pos(action[3][0], action[3][1])
            if self.board.get_color(_from.x, _from.y) != self.color or self.board.get_color(_to.x, _to.y) == opposite(self.color):
                return False
            if self.board.get_num(_from.x, _from.y) < _n or 0 >= _n:
                return False
            if _to not in _from.card_neighbour(self.board.get_num(_from.x, _from.y)):
                return False
        elif action[0] == "BOOM":
            if self.board.get_color(action[1][0], action[1][1]) != self.color:
                return False
        return True
