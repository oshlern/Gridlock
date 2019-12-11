from cards import *
import random


class Place:
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
    def set_card(self, card):
        self.card = card
        card.place = self

class Board:
    def __init__(self, size, game):
        self.deck = game.deck
        self.size = size
        self.array = [[Place() for j in range(size)] for i in range(size)]

        for i in range(size):
            for j in range(size):
                neighbors = []
                if i > 0:
                    neighbors.append(self.array[i-1][j])
                if i < size - 1:
                    neighbors.append(self.array[i+1][j])
                if j > 0:
                    neighbors.append(self.array[i][j-1])
                if j < size - 1:
                    neighbors.append(self.array[i][j+1])
                self.array[i][j].neighbors = neighbors

                self.deck.draw(self.array[i][j])

        self.rows = [row for row in self.array] + [[self.array[i][j] for i in range(size)] for j in range(size)]
        self.squares = [[self.array[i][j], self.array[i+1][j], self.array[i][j+1], self.array[i+1][j+1]] for i in range(size-1) for j in range(size-1)]
        self.diagonals = [[self.array[i][i] for i in range(size)], [self.array[size-1-i][i] for i in range(size)]]

    def __str__(self):
        return '   ' + '\t '.join([str(i) for i in range(self.size)]).expandtabs(16) + '\n' \
                + '\n'.join(str(i) + ' |' + '\t|'.join([str(place.card) for place in row]).expandtabs(16) for i,row in enumerate(self.array))

    def place_card(self, hand_card, i, j):
        location = self.array[i][j]
        board_card = location.card

        if not swappable(hand_card, board_card):
            raise TypeError("Cannot swap {} and {}".format(hand_card, board_card))

        hand_card.place.cards.remove(hand_card)
        location.set_card(hand_card)
        self.deck.set_card(board_card)

class Deck:
    colors = ["Red", "Green", "Blue", "Yellow"]
    def __init__(self):
        #card generation
        self.cards = []
        for color in self.colors*2:
            for number in range(10):
                self.cards.append(NumberCard(self, color, number))
            for Special in [SkipCard, PlusTwoCard, ReverseCard]:
                self.cards.append(Special(self, color))
        for _ in range(4):
            self.cards.append(WildCard(self))
            self.cards.append(PlusFourCard(self))

    def draw(self, location):
        index = random.randrange(len(self.cards))
        location.set_card(self.cards.pop(index))

    def set_card(self, card):
        self.cards.append(card)
        card.place = self

class Hand:
    def __init__(self, num_cards, deck):
        self.num_cards = num_cards
        self.deck = deck
        self.cards = []
        for num in range(num_cards):
            deck.draw(self)

    def set_card(self, card):
        self.cards.append(card)
        card.place = self

    def __str__(self):
        return '|'.join([str(card) for card in self.cards])





