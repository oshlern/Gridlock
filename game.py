from cards import *
from place import *
from player import *
import itertools

# print(locals())
# exec("x = 2\ndef y():\n\tpass")
# print(locals())
# print(x)
# print(y)
# def a():
#     exec('def win_cond(board):\n\tfor region in board.squares:\n\t\tif 9 in get_potential_sums(squares) or 10 in get_potential_sums(squares) or 8 in get_potential_sums(squares):\n\t\t\treturn True\n\treturn False')
#     print(win_cond)
# a()

class Game():
    def __init__(self, num_players, b_dimension):
        self.deck = Deck()
        self.board = Board(b_dimension, self)
        self.players = [Player("Player {}".format(num), self) for num in range (num_players)]
        self.set_win_conditions(num_players)
    
    def set_board(self, board):
        self.board = board

    def set_win_conditions(self, num_players):
        self.win_conditions = [self.generate_win_condition(), self.generate_win_condition()]
        for i in range(num_players):
            self.players[i].set_win_condition(self.win_conditions[i%2])

    def generate_win_condition(self):
        region = random.choice(["rows", "diagonals", "squares"])
        num_targets = random.choice([1,2])
        cond_type = random.choice(["numbers", "colors"])

        win_cond_str = ("def _win_cond(board):\n"
                        "\tcount = 0\n"
                        "\tfor region in board.{0}:\n"
                            "\t\tif").format(region)
        description = "{0} {1}".format(num_targets, region)

        if cond_type == "numbers":
            sub_type_options = ["sum", "multiple", "consecutive"]
            num_type = random.choice(sub_type_options)
            if num_type == "sum":
                num = random.choice(list(range(5,11)) + list(range(25, 30)))
                description += " must sum to {}+-1".format(num)
                win_cond_str += (" {0} in get_potential_sums(region) or {1} in get_potential_sums(region) or {2} in get_potential_sums(region):\n").format(num, num+1, num-1)
            elif num_type == "multiple":
                num = random.choice(range(3,6))
                description += " must have a sum that is a multiple of {0}".format(num)
                win_cond_str += (" any([sum % {0} == 0 for sum in get_potential_sums(region)]):\n").format(num)
            elif num_type == "consecutive":
                description += " must have consecutive numbers"
                win_cond_str += (" is_consecutive(region):\n").format(region)
                #invalid syntax error on this version:
                #any([all([sorted(reg)[i] < sorted(reg)[i+1] and sorted(reg)[i] - sorted(reg)[i+1] == -1 for i in range(len(reg)-1)]) for reg in board.{0}])
        elif cond_type == "colors":
            color_type = random.choice(["num of 1", "1 of each"])
            if color_type == "1 of each":
                description += " must have one of each color"
                colors = ["'red'", "'green'", "'blue'", "'yellow'"]
                win_cond_str += " any([all([color in region_colors for color in colors]) for region_colors in get_potential_colors(region)]):\n"
            elif color_type == "num of 1":
                color = random.choice(["red", "green", "blue", "yellow", "special"])
                num = random.choice(range(2,5))
                description += " must have {0} {1} cards".format(num, color)
                win_cond_str += " count_color(region, {0}) == {1}:\n".format(color, num)
        win_cond_str += ("\t\t\tcount +=1\n"
                    "\treturn count >= {0}").format(num_targets)
        
        print("DEGBUG:", win_cond_str.__repr__()) #for testing, comment in final version
        exec(win_cond_str, globals(), locals()) #not working for some reason
        # print(locals()['win_cond'])
        win_cond = locals()['_win_cond']
        win_cond.description = description
        return win_cond






def get_potential_num_combs(region):
    return itertools.product(*[place.card.get_potential_numbers() for place in region])

def get_potential_sums(region):
    potential_sums = [sum(nums) for nums in get_potential_num_combs(region)]
    return potential_sums

def get_potential_colors(region):
    return itertools.product(*[place.card.get_potential_colors() for place in region])

def count_color(region, color):
    if color == "special":
        return sum([place.card.special for place in region])
    return sum([color in place.card.get_potential_colors() for place in region])

def is_consecutive(region):
    any_consecutive = False
    for reg in get_potential_num_combs(region):
        reg = sorted(reg)
        prev = reg[0]
        consecutive = True
        for i in range(1,len(reg)):
            if reg[i]-prev != 1:
                consecutive = False
            prev = reg[i]
        if consecutive:
            any_consecutive = True
    return any_consecutive



# region = place.attrs[region_str]
# if 
# def condition(region)
# def win_cond(board):
#     return sum(condition(region) for region in regions) >= num_targets