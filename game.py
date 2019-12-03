from cards import *
from place import *
from player import *
import itertools

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

    def generate_win_condition(self):
        region = random.choice(["rows", "diagonals", "squares"])
        num_targets = random.choice([1,2])
        cond_type = random.choice(["numbers", "colors"])

        win_cond_str = ("def win_cond(board):"
                        "\tfor region in board.{0}:"
                            "\t\tif").format(region)
        description = "{0} {1}".format(num_targets, region)

        if cond_type == "numbers":
            sub_type_options = ["sum", "multiple", "consecutive"]
            num_type = random.choice(sub_type_options)
            if num_type == "sum":
                num = random.choice(list(range(5,11)) + list(range(25, 30)))
                description += " must sum to {}+-1".format(num)
                win_cond += ("{0} in get_potential_sums({1}) or {2} in get_potential_sums({1}) or {3} in get_potential_sums({1}):"
                                "\t\t\t return True"
                                "\t return False").format(num, region, num+1, num-1)
            elif num_type == "multiple":
                num = random.choice(range(3,6))
                description += " must have a sum that is a multiple of {0}".format(num)
                win_cond += ("get_potential_sums({0}) % {1} == 0:"
                                "\t\t\t return True"
                                "\t return False").format(region, num)
            elif num_type == "consecutive":
                description += " must have consecutive numbers"
                #ADD
        elif cond_type == "colors":
            color_type = random.choice(["num of 1", "1 of each"])
            if color_type == "1 of each":
                description += " must have one of each color"
            elif color_type == "num of 1":
                color = random.choice(["red", "green", "blue", "yellow", "special"])
                num = random.choice(range(2,5))
                description += " must have {0} {1} cards".format(num, color)
        exec(win_cond_str)
        win_cond.description = description
        return win_cond
                



 ## example, squares must add up to 25
def get_potential_num_combs(region):
    return itertools.product(place.card.get_potential_numbers() for place in region)

def get_potential_sums(region):
    potential_sums = [sum(nums) for nums in get_potential_num_combs(region)]
    return potential_sums

def get_potential_colors(region):
    potential_colors = [place.card.get_potential_colors() for place in region]
    return itertools.product(*potential_colors)

#def wincond(board): example
 #   for region in board.squares: #.region changes based on cond
 #       if get_sum(region) == 25: #this whole if statement will change
 #           return True
 #   return False