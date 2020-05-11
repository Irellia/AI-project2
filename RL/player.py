from _404NotFound_ import player
import pickle

class Player(player.Player):

    def __init__(self, color):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """
        # os.chdir("..")
        # my_file = os.path.join(os.path.join("RL"), '_500_lr=02.pickle')
        super().__init__(color)
        with open("RL/train/500_lr=05_eval0234.pickle", "rb") as f:
            self.state_values = pickle.load(f)[0] if color == "white" else pickle.load(f)[1]

        # with open("RL/train/_1_lr=02.pickle", "rb") as f:
        #     self.agents = pickle.load(f)[0] if color == "white" else pickle.load(f)[1]


    def add_state_value(self, v):
        pass

    def add_history(self, h):
        pass

    def reset_history(self):
        pass

    def update_state_values(self, referee):
        pass


