class Card:
    def __init__(self, place = deck):
        self.place = place

    def get_colors(self):
        return [self.color]

    def get_numbers(self):
        return [self.number]

    def get_num_cols(self, places_visited=[]):
        return zip(get_numbers(self), get_colors(self))

    def get_neighbor_numbers(self, places_visited=[]):
        # numbers = []
        # new_places_visited = places_visited + [self.place]
        # for place in self.place.neighbors:
        #     if place in places_visited:
        #         continue
        #     numbers += [num for num in place.card.get_numbers(new_places_visited)]
        # return numbers
        return sum([place.card.get_numbers(places_visited + [self.place]) for place in self.place.neighbors if place not in places_visited], [])

    def get_neighbor_colors(self, places_visited=[]):
        return sum([place.card.get_colors(places_visited + [self.place]) for place in self.place.neighbors if place not in places_visited], [])

    def get_neighbor_nums_and_cols(self, places_visited=[]):
        return sum([place.card.get_nums_and_cols(places_visited + [self.place]) for place in self.place.neighbors if place not in places_visited], [])

    def nums_and_cols(self, places_visited=[]): pass
    def get_colors(self): pass
    def get_numbers(self): pass
    def get_place(self):
        return self.place

class PlainCard(Card):
    def __init__(self, place, number, color):
        self.number = number
        self.color = color

#     def get_colors(self):
#         return [self.color]



class ReverseCard(Card):
    def __init__(self, color):
        self.color = color
        self.number = 0

    def special_action(neighbor):
        assert neighbor in self.place.neighbors, "this place is not a neigbor of the reverse"
        self.place.card, neighbor.card = neighbor.card, self

class SkipCard(Card):
    def __init__(self, color):
        self.color = color

    def get_num_cols(self, places_visited=[]):
        return [[self.color, number] for number in self.get_numbers(places_visited)]

    def get_numbers(self, places_visited=[]):
        return [-num for num in self.get_neighbor_numbers(places_visited)] 

    def get_colors(self):
        return [self.color]

class WildCard(Card):
    def get_numbers(self, places_visited=[]):
        return self.get_neighbor_numbers(places_visited)

    def get_colors(self, places_visited=[]):
        return self.get_neighbor_colors(places_visited)

    def get_num_cols(self, places_visited=[]):
        return [(num, col) for num in self.get_numbers(places_visited) for col in self.get_colors(places_visited)]

class PlusTwo(Card):
    def __init__(self, place=deck):
        super().__init__(place=place)

class PlusFour(Card):
    def 
class Place:

    def __init__(neighbors = [] card = None):
        self.neighbors = neighbors
        self.card = card
    def set_
    def set_card(self, card):
        self.card = card


def can_substitue(card1, card2):
    if card1.wild or card2.wild:
        return True
    if card1.color == card2.color:
        return True
    if 

"""
Places and cards are classes
A place has neighbors and its card as attributes. 
    method to get neighbors that takes in list of already visited places (make sure list)
"""


