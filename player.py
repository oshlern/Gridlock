from place import *

class Player():
    def __init__(self, name, game, team_num):
        self.hand = Hand(5, game.deck)
        self.name = name
        self.game = game
        self.team_num = team_num

    def set_win_condition(self, win_condition):
        self.win_condition = win_condition
        self.display(win_condition.description)

    def display(self, string):
        print("------{}: {}".format(self.name, string))

    def take_turn(self):
        self.display("your objective")
        print(self.win_condition.description)
        self.display("your hand")
        print(self.hand)
        self.display("the board")
        print(self.game.board)
        invalid1 = True
        while invalid1:
            self.display("which card would you like to play from your hand?")
            self.game.graphics.display_instruction("which card would you like to play from your hand?")
            #inp = input()
            on_board, on_hand, on_deck, coord = self.game.graphics.get_card_selection()
            board_reverse = False
            try:
                if on_board:
                    i, j = int(coord[0]), int(coord[1])
                    if self.game.board.is_reverse(i, j):
                        card = self.game.board.array[i][j].card
                        board_reverse = True
                        invalid1 = False
                elif on_hand:
                    card = self.hand.cards[int(coord)]
                    board_reverse = False
                    invalid1 = False

                if invalid1:
                    print("invalid selection, click a card in the hand or a reverse card")
                    self.game.graphics.display_status("invalid selection, click a card in the hand or a reverse card")
                    
            except (IndexError, ValueError) as e:
                self.display("invalid card")
                self.game.graphics.display_status("invalid card")
                print(e)

        invalid2 = True
        while invalid2:
            self.display("where would you like to put it? (row, column)")
            self.game.graphics.display_instruction("where would you like to put it?")
            on_board, on_hand, on_deck, coord = self.game.graphics.get_card_selection()
            if on_deck and not board_reverse:
                self.game.deck.set_card(card)
                self.hand.cards.remove(card)
                invalid2 = False
            elif on_board:
                try: 
                    self.game.board.place_card(card, int(coord[0]), int(coord[1]), board_reverse)
                    invalid2 = False
                except (IndexError, ValueError) as e:
                    self.display("invalid placement")
                    self.game.graphics.display_status("invalid placement")
                    print(e)
                except TypeError as e:
                    self.game.graphics.display_status(str(e))

            if invalid2:
                print("invalid selection, click a card on the board")
                self.game.graphics.display_status("invalid selection, click a card on the board")
            elif not board_reverse:
                self.game.deck.draw(self.hand)
        self.game.graphics.display_always()

