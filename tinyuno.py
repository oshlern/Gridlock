import random

# win_conditions 

# num_condition = [
#     "A row and a col sum to ",
#     "Sum is divisible by",
#     "Two rows have the same sum",
    
# ]

# color_condition = [
#     "Each diagonal has all colors",
#     ""
# ]

def generate_win_cond():
    region = random.choice(["row", "diagonal", "square"])
    num_targets = random.choice([1,2])
    cond_type = random.choice(["numbers", "colors"])
    if cond_type == "numbers":
        sub_type_options = ["sum", "multiple", "consecutive"]
        # if num_targets:
            # sub_type_options += ["same sum"]
        num_type = random.choice(sub_type_options)
        if num_type == "sum":
            amount = random.choice(list(range(5,11)) + list(range(25, 30)))
            return "{} {}(s) sums to {}".format(num_targets, region, amount)
        elif num_type == "multiple":
            num = random.choice(range(3,6))
            return "{} {}(s) sums to a multiple of {}".format(num_targets, region, num)
        elif num_type == "consecutive":
            return "{} {}(s) must have consecutive numbers".format(num_targets, region)
    elif cond_type == "colors":
        color_type = random.choice(["num of 1", "1 of each"])
        if color_type == "1 of each":
            if num_targets == 1:
                return "A {} must have 1 of each color".format(region)
            elif num_targets == 2:
                return "2 {}s must each have 1 of each color".format(region)
        elif color_type == "num of 1":
            color = random.choice(["red", "green", "blue", "yellow", "special"])
            if num_targets == 1:
                return "A {} must have 3 {} cards".format(region, color)
            elif num_targets == 2:
                return "2 {}s must each have 3 {} cards".format(region, color)



# def generate_sum():

# class WinCond:

# Number, Color, Combo

# class RowCond(WinCond):

#     def cond(self, row):
#         raise NotImplementedError

#     def is_met(self, board):
#         for row in rows (cols)
#             if self.cond(row):
#                 return True
#         return False

# class Sum(RowCond):
#     def __init__(self, amount):
#         self.amount = amount

#     def cond(self, row):
#         return sum(row) == self.amount

# class DiagCond(WinCond):

