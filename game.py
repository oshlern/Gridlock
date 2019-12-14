from cards import *
from place import *
from player import *
from graphics import *
import itertools

class Game():
    def __init__(self, num_players, b_dimension, goal):
        self.deck = Deck()
        self.board = Board(b_dimension, self)
        self.players = [Player("Player {}".format(num), self) for num in range (num_players)]
        self.set_win_conditions()
        self.goal = goal
        self.graphics = Graphics(self.board)

    def set_board(self, board):
        self.board = board

    def set_win_conditions(self):
        self.win_conditions = []
        for _ in range(2):
            win_cond = self.generate_win_condition()
            while win_cond(self.board):
                # print("ditching:", win_cond.description) #testing
                win_cond = self.generate_win_condition()
            self.win_conditions.append(win_cond)

        # self.win_conditions = [self.generate_win_condition(), self.generate_win_condition()]
        for i in range(len(self.players)):
            self.players[i].set_win_condition(self.win_conditions[i%2])

    def generate_win_condition(self):
        region = random.choice(["rows", "diagonals", "squares"])
        num_targets = random.choice([1,2])
        cond_type = random.choice(["numbers", "colors"])
        point_value = 1

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
                win_cond_str += " is_consecutive(region):\n"
                #invalid syntax error on this version:
                #any([all([sorted(reg)[i] < sorted(reg)[i+1] and sorted(reg)[i] - sorted(reg)[i+1] == -1 for i in range(len(reg)-1)]) for reg in board.{0}])
        elif cond_type == "colors":
            color_type = random.choice(["num of 1", "1 of each"])
            if color_type == "1 of each":
                description += " must have one of each color"
                win_cond_str += " has_one_of_each(region):\n"
            elif color_type == "num of 1":
                color = random.choice(["'Red'", "'Green'", "'Blue'", "'Yellow'", "'special'"])
                num = random.choice(range(2,5))
                description += " must have {0} {1} cards".format(num, color)
                win_cond_str += " count_color(region, {0}) == {1}:\n".format(color, num)
        win_cond_str += ("\t\t\tcount +=1\n"
                    "\treturn count >= {0}").format(num_targets)

        # print("DEBUG:", win_cond_str) #for testing, comment in final version
        # print("DEBUG:", locals())
        exec(win_cond_str, globals(), locals())
        # print(locals()['win_cond'])
        win_cond = locals()['_win_cond']
        win_cond.description = description
        win_cond.point_value = point_value
        return win_cond

    def play(self):
        player_num = -1
        while not any([win_cond(self.board) for win_cond in self.win_conditions]):
            player_num = (player_num + 1) % len(self.players)
            self.players[player_num].take_turn()
        if self.win_conditions[0](self.board):
            print("------Players {} win this round!".format([i for i in range(0,len(self.players),2)]))
            for i in range(0, len(self.players), 2):
                self.players[i].points += self.win_conditions[0].point_value
        if self.win_conditions[1](self.board):
            print("------Players {} win this round!".format([i for i in range(1,len(self.players),2)]))
            for i in range(1, len(self.players), 2):
                self.players[i].points += self.win_conditions[1].point_value
    
    def play_with_points(self):
        self.play()
        while not any([player.points >= self.goal for player in self.players]):
            self.set_win_conditions()
            self.play()
        for player in self.players:
            if player.points >= self.goal:
                print("------{0} wins the game!".format(player.name))





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

def has_one_of_each(region):
    colors = ["Red", "Green", "Blue", "Yellow"]
    return all([count_color(region, color) >= 1 for color in colors])

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