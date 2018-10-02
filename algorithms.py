from random import *
import collections

class Algorithms():
    def pure_random(self, actions_dict):
        #total_options = sum(game_state.values())
        total_options = sum({key: len(value) for key, value in actions_dict.items()}.values())
        print("Total options: " + str(total_options))
        if total_options == 1:
            return 1
        if total_options < 1:
            return -1
        return randint(1, total_options)

