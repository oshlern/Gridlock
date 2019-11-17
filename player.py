from place import *

class Player():
    def __init__(self, name, game):
        self.hand = Hand(5, game.deck)
        self.name = name
        
    def set_win_condition(win_condition):
        self.win_condition = win_condition
        self.display(win_condition_description)

    def display(self, string):
        print("{}: {}".format(self.name, string))

    def take_turn(self):
        input()