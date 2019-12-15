from cards import *
from place import *
from player import *
from graphics import *
import itertools

class Game():
    def __init__(self, players=2, b_dimension = 4, goal = 3):
        self.goal = goal
        self.deck = Deck()
        self.board = Board(b_dimension, self)

        if type(players) == int:
            names = ["Player {}".format(num) for num in range(players)]
        elif type(players) == list:
            names = players
        self.num_players = len(names)
        self.players = [Player(names[num], self, num%2) for num in range(self.num_players)]
        self.teams = [[self.players[i] for i in range(0,self.num_players,2)], [self.players[i] for i in range(1,self.num_players,2)]]

        self.graphics = Graphics(self, fullscreen=False)
        # self.graphics.display_board()

    def set_board(self, board):
        self.board = board

    def set_win_conditions(self):
        self.win_conditions = []
        for _ in range(2):
            win_cond = self.generate_win_condition()
            while win_cond(self.board):
                win_cond = self.generate_win_condition()
            self.win_conditions.append(win_cond)
        if self.win_conditions[0].description == self.win_conditions[1].description:
            self.set_win_conditions()
        for i in range(self.num_players):
            self.players[i].set_win_condition(self.win_conditions[i%2])

    def generate_win_condition(self):
        region = random.choice(["rows", "diagonals", "squares"])
        num_targets = random.choice([1,2])
        cond_type = random.choice(["numbers", "colors"])
        point_value = num_targets

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
                win_cond_str += " has_num_color(region, {0}, {1}):\n".format(color, num)
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

    def play_round(self):
        player_num = -1
        self.set_win_conditions()
        self.graphics.display_always()
        while not any([win_cond(self.board) for win_cond in self.win_conditions]):
            player_num = (player_num + 1) % self.num_players
            self.graphics.display_player(self.players[player_num])
            self.players[player_num].take_turn()
        for team_num in range(2):
            if self.win_conditions[team_num](self.board):
                self.points[team_num] += self.win_conditions[team_num].point_value
                self.graphics.display_status("{} win this round!".format(', '.join([player.name for player in self.teams[team_num]])))
                print("------{} win this round!".format([player.name for player in self.teams[team_num]]))
                self.graphics.display_instruction("click for next round")
                self.graphics.wait_for_click()

        # if self.win_conditions[0](self.board):
        #     print("------Players {} win this round!".format([i for i in range(0,self.num_players,2)]))
        #     self.graphics.display_message("Players {} win this round!".format([i for i in range(0,self.num_players,2)]))
        #     for i in range(0, self.num_players, 2):
        #         self.players[i].points += self.win_conditions[0].point_value
        # if self.win_conditions[1](self.board):
        #     print("------Players {} win this round!".format([i for i in range(1,self.num_players,2)]))
        #     self.graphics.display_message("Players {} win this round!".format([i for i in range(1,self.num_players,2)]))
            
        #     for i in range(1, self.num_players, 2):
        #         self.players[i].points += self.win_conditions[1].point_value

    def play_with_points(self):
        self.points = [0, 0]
        while not any([team_points >= self.goal for team_points in self.points]):
            self.play_round()
        if self.points[0] >= self.goal and self.points[1]< self.goal:
            winners = ', '.join([player.name for player in self.teams[0]])
            print("------{} win the game!".format(winners))
            # self.graphics.display_status("{} win the game!".format(winners))
        elif self.points[1] >= self.goal and self.points[0] < self.goal:
            winners = ', '.join([player.name for player in self.teams[1]])
            print("------Players {} win the game!".format(winners))
            # self.graphics.display_status("{} win the game!".format(winners))
        else:
            winners = ', '.join([player.name for player in self.players])
            print("it's a tie!")
            # self.graphics.display_status("its a tie!")

        self.graphics.display_win(winners)





def get_potential_num_combs(region):
    return itertools.product(*[place.card.get_potential_numbers() for place in region])

def get_potential_sums(region):
    potential_sums = [sum(nums) for nums in get_potential_num_combs(region)]
    return potential_sums

def get_potential_colors(region):
    return itertools.product(*[place.card.get_potential_colors() for place in region])

def has_num_color(region, color, num):
    if color == "special":
        return sum([place.card.special for place in region])
    for potential_colors in get_potential_colors(region):
        if sum([color == potential_color for potential_color in potential_colors]) == num:
            return True
    return False

def has_one_of_each(region):
    colors = ["Red", "Green", "Blue", "Yellow"]
    for potential_colors in get_potential_colors(region):
        if all([color in potential_colors for color in colors]):
            return True
    return False

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



if __name__ == "__main__":
    game = Game()
    game.play_with_points()


# region = place.attrs[region_str]
# if 
# def condition(region)
# def win_cond(board):
#     return sum(condition(region) for region in regions) >= num_targets