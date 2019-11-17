from cards import *
from place import *
from player import *

class Game():
    def __init__(self, num_players, b_dimension):
        self.deck = Deck()
        self.board = Board(b_dimension, self)
        self.players = [Player("Player {}".format(num), self) for num in range (num_players)]
        # self.set_win_conditions(num_players)

    def set_board(self, board):
        self.board = board

    def set_win_conditions(self, num_players):
        self.win_conditions = [generate_win_condition() for player in self.players]
        for i in range(num_players):
            self.players[i].set_win_condition(self.win_conditions[i])

    def generate_win_condition():
        region = random.choice(["row", "diagonal", "square"])
        num_targets = random.choice([1,2])
        cond_type = random.choice(["numbers", "colors"])

        win_cond = "for region in board.{0}s:".format(region)
        description = "{}".format(region)

        if cond_type == "numbers":
            sub_type_options = ["sum", "multiple", "consecutive"]
            num_type = random.choice(sub_type_options)
            if num_type == "sum":
                num = random.choice(list(range(5,11)) + list(range(25, 30)))
                description += "must sum to {}+-1".format(num)
            elif num_type == "multiple":
                num = random.choice(range(3,6))
            elif num_type == "consecutive":
        elif cond_type == "colors":
            color_type = random.choice(["num of 1", "1 of each"])
            if color_type == "1 of each":
            elif color_type == "num of 1":
            color = random.choice(["red", "green", "blue", "yellow", "special"])
                


        
        win_cond += "\t"
        
        
        


