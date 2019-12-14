from place import *

class Player():
    def __init__(self, name, game):
        self.hand = Hand(5, game.deck)
        self.name = name
        self.game = game
        self.points = 0

    def set_win_condition(self, win_condition):
        self.win_condition = win_condition
        self.display(win_condition.description)

    def display(self, string):
        print("------{}: {}".format(self.name, string))

    def take_turn(self):
        self.display("your objective")
        print(self.win_condition.description)
        self.display("your hand")
        self.game.graphics.display_hand(self.hand)
        print(self.hand)
        self.display("the board")
        self.game.graphics.display_board()
        print(self.game.board)
        invalid1 = True
        while invalid1:
            self.display("which card would you like to play from your hand? (number from the left starting at 0, or reverse)")
            #inp = input()
            on_board, coord = self.game.graphics.get_card_selection()
            if on_board:
                print("invalid selection, click a card in the hand")
                continue
            try:
                card = self.hand.cards[int(coord)]
                invalid1 = False
            except (IndexError, ValueError) as e:
                self.display("invalid card")
                print(e)
        invalid2 = True
        while invalid2:
            self.display("where would you like to put it? (row, column)")
            on_board, coord = self.game.graphics.get_card_selection()
            if not on_board
                print("invalid selection, click a card on the board")
                continue
            try: 
                self.game.board.place_card(card, int(coord[0]), int(coord[1]))
                invalid2 = False
            except (TypeError, IndexError, ValueError) as e:
                self.display("invalid placement")
                print(e)
        self.game.deck.draw(self.hand)
        self.game.graphics.display_board()

