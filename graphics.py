import pygame
import os
     
    # main loop
    #while running:
        # event handling, gets all event from the event queue
        #for event in pygame.event.get():
            # only do something if the event is of type QUIT
            #if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                #running = False
        # makes updates to the game screen visible (?)
        #pygame.display.flip()


class Graphics:
    def __init__(self, board):
        self.board = board
        self.screen_width = 1000
        self.screen_height = 700
        self.card_height = int(self.screen_height * .75 / board.size)
        self.card_width = int(self.card_height * 82/117)
        self.board_x = 20
        self.board_y = 20
        self.hand_x = 20
        self.hand_y = self.screen_height - self.card_height 

        pygame.init()
        pygame.display.set_caption("Gridlock")
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.image_library = {name: self.scale(pygame.image.load("uno_cards/" + name)) for name in os.listdir("uno_cards/")}
        self.display_board()

    def scale(self, image):
        image = pygame.transform.scale(image, (self.card_width, self.card_height))
        return image

    def display_board(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                card_image = self.image_library[self.board.array[i][j].card.image_file]
                self.screen.blit(card_image, (self.board_x + i*self.card_width , self.board_y + j * self.card_height ))
        pygame.display.flip()

    def display_hand(self, hand):
        for i in range(len(hand.cards)):
            card_image = self.image_library[hand.cards[i].image_file]
            self.screen.blit(card_image, (self.hand_x + i*self.card_width, self.hand_y))
        pygame.display.flip()
            

    def get_card_selection(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    on_board, on_hand, coord = self.translate_coord(x, y)
                    if on_board or on_hand:
                        return on_board, coord

    def translate_coord(self, x, y):
        board_i, board_j = (x-self.board_x)//self.card_width, (y-self.board_y)//self.card_height
        hand_i, hand_j = (x-self.hand_x)//self.card_width, (y-self.hand_y)//self.card_height
        on_board, on_hand, coord = False, False, None
        if 0<=board_i<self.board.size and 0<=board_j<self.board.size:
            on_board = True
            coord = (board_i, board_j)
        elif 0 <= hand_i <= 5 and 0 <= hand_j <= 1:
            on_hand = True
            coord = hand_i
        return on_board, on_hand, coord
