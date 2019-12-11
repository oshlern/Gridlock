class Card:
    special = False
    def __init__(self, place, s_color, s_id):
        self.place = place
        self.s_color = s_color
        self.s_id = s_id

    def get_potential_colors(self, places_visited = []):
        return []
    def get_potential_numbers(self, places_visited = []):
        return []
    def get_potential_pairs(self, places_visited = []):
        return [()]

    def get_neighbor_colors(self, places_visited = []):
        return list(set(sum([place.card.get_potential_colors(places_visited + [self.place]) for place in self.place.neighbors if place not in places_visited], [])))
    def get_neighbor_numbers(self, places_visited = []):
        return list(set(sum([place.card.get_potential_numbers(places_visited + [self.place]) for place in self.place.neighbors if place not in places_visited], [])))
    def get_neighbor_pairs(self, places_visited = []):
        return list(set(sum([place.card.get_potential_pairs(places_visited + [self.place]) for place in self.place.neighbors if place not in places_visited], [])))
    def __repr__(self):
        return "{0} {1}".format(self.s_color, self.s_id)


class NumberCard(Card):
    def get_potential_colors(self, places_visited = []):
        return [self.s_color]
    def get_potential_numbers(self, places_visited = []):
        return [self.s_id]
    def get_potential_pairs(self, places_visited = []):
        return [(self.s_color, self.s_id)]

class ReverseCard(Card):
    special = True
    def __init__(self, place, s_color):
        super().__init__(place, s_color, s_id = "Reverse")
        
    def get_potential_colors(self, places_visited = []):
        return [self.s_color]
    def get_potential_numbers(self, places_visited = []):
        return [0]
    def get_potential_pairs(self, places_visited = []):
        return [(self.s_color, 0)]

    def special_action(self, neighbor):
        assert neighbor in self.place.neighbors, "this place is not a neigbor of the reverse"
        self.place.card, neighbor.card = neighbor.card, self

class SkipCard(Card):
    special = True

    def __init__(self, place, s_color):
        super().__init__(place, s_color, s_id = "Skip")
        
    def get_potential_colors(self, places_visited = []):
        return [self.s_color]
    def get_potential_numbers(self, places_visited = []):
        return [-number for number in self.get_neighbor_numbers(places_visited)] 
    def get_potential_pairs(self, places_visited = []):
        return [(self.s_color, number) for number in self.get_potential_numbers(places_visited)]

class PlusTwoCard(Card):
    special = True

    def __init__(self, place, s_color):
        super().__init__(place, s_color, s_id = "PlusTwo")

    def get_potential_colors(self, places_visited = []):
        return [self.s_color]
    def get_potential_numbers(self, places_visited = []):
        return [number + 2 for number in self.get_neighbor_numbers(places_visited)] 
    def get_potential_pairs(self, places_visited = []):
        return [(self.s_color, number) for number in self.get_potential_numbers(places_visited)]


class WildCard(Card):
    special = True

    def __init__(self, place):
        super().__init__(place, s_color = "Wild", s_id = "Wild")

    def get_potential_colors(self, places_visited = []):
        return self.get_neighbor_colors(places_visited)
    def get_potential_numbers(self, places_visited = []):
        return self.get_neighbor_numbers(places_visited)
    def get_potential_pairs(self, places_visited = []):
        return [(color, number) for color in self.get_potential_colors(places_visited) for number in self.get_potential_numbers(places_visited)]

class PlusFourCard(Card):
    special = True

    def __init__(self, place):
        super().__init__(place, s_color = "Wild", s_id = "PlusFour")

    def get_potential_colors(self, places_visited = []):
        return self.get_neighbor_colors(places_visited)
    def get_potential_numbers(self, places_visited = []):
        neighbor_numbers = self.get_neighbor_numbers(places_visited)
        return [number + 4 for number in neighbor_numbers] + [number - 4 for number in neighbor_numbers]
    def get_potential_pairs(self, places_visited = []):
        neighbor_pairs = self.get_neighbor_pairs(places_visited)
        return [(color, number + 4) for color,number in neighbor_pairs] + [(color, number - 4) for color,number in neighbor_pairs]

def swappable(card1, card2):
    if card1.s_color == "Wild" or card2.s_color == "Wild":
        return True
    if card1.s_color == card2.s_color or card1.s_id == card2.s_id:
        return True
    return False