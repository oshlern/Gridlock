from cards import *
import random


class Place:
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
    def set_card(self, card):
        self.card = card
        card.place = self

class Board:
    def __init__(self, width, height):
        self.deck = Deck()
        self.width = width
        self.height = height
        self.array = [[Place() for j in range(width)] for i in range(height)]

        for i in range(height):
            for j in range(width):
                neighbors = []
                if i > 0:
                    neighbors.append(self.array[i-1][j])
                if i < height - 1:
                    neighbors.append(self.array[i+1][j])
                if j > 0:
                    neighbors.append(self.array[i][j-1])
                if j < width - 1:
                    neighbors.append(self.array[i][j+1])
                self.array[i][j].neighbors = neighbors

                self.deck.draw(self.array[i][j])

    def __str__(self):
        return '\n'.join('\t|'.join([str(place.card) for place in row]).expandtabs(16) for row in self.array)

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
    def set_card(self, card):
        self.cards.append(card)
        card.place = self





