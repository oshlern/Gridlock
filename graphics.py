import pygame
import os, time, sys

card_ratio = 82/117
clock = pygame.time.Clock()
fps = 30
hand_size = 5

class Graphics:
    def __init__(self, game, fullscreen=False):
        self.game = game
        self.board = game.board

        pygame.init()
        pygame.display.set_caption("Gridlock")
        if fullscreen:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            self.screen_width, self.screen_height = self.screen.get_size()
        else:
            self.screen_width, self.screen_height = 1000, 700
            self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))

        self.board_height = int(0.75 * self.screen_height)
        self.board_width = int(card_ratio * self.board_height)
        self.card_height, self.card_width = int(self.board_height / self.board.size), int(self.board_width / self.board.size)
        self.board_x, self.board_y = 20, 20
        self.hand_x, self.hand_y = self.board_x, self.screen_height - self.board_y - self.card_height
        self.deck_x, self.deck_y = self.hand_x + (1+hand_size)*self.card_width, self.hand_y
        self.deck_width = self.card_width*0.4

        self.team_colors = [(40,60,255), (255,60,40)]

        self.image_library = {name: self.scale(pygame.image.load("uno_cards/" + name)) for name in os.listdir("uno_cards/")}
        self.display_screen()

    def scale(self, image):
        image = pygame.transform.scale(image, (self.card_width, self.card_height))
        return image

    def display_board(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                card_image = self.image_library[self.board.array[i][j].card.image_file]
                self.screen.blit(card_image, (self.board_x + i*self.card_width , self.board_y + j * self.card_height ))

    def display_deck(self):
        card_image = self.image_library["uno_card-back.png"]
        num_displayed = 4
        for i in range(num_displayed):
            offset = int(i/num_displayed * self.deck_width)
            self.screen.blit(card_image, (self.deck_x + offset, self.deck_y + i))

    def clear_background(self):
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(0, 0, self.screen_width, self.screen_height))

    def display_win(self, winners):
        self.clear_background()
        font = pygame.font.Font(None, 100)
        message = font.render("THE WINNERS ARE:", True, (255,255,255), (0,0,0))
        x = (self.screen_width - message.get_width())//2
        y = (self.screen_height/2 - message.get_height())//2
        self.screen.blit(message, (x, y))
        self.display_screen()
        self.wait_for_click()

        font = pygame.font.Font(None, 300//(1+len(winners)//8))
        message = font.render(winners, True, (255,255,255), (0,0,0))
        x = (self.screen_width - message.get_width())//2
        y = (self.screen_height - message.get_height())//2
        self.screen.blit(message, (x, y))
        self.display_screen()
        self.wait_for_click()


    def display_always(self):
        self.clear_background()
        self.display_board()
        self.display_deck()

        section_spacer = 50
        parent_child_spacer = 35
        child_spacer = 25

        title_y = self.board_y
        self.display_message("GRIDLOCK",  y = title_y, font = 50)

        section_y = title_y + section_spacer
        child1_y = section_y + parent_child_spacer
        child2_y = child1_y + child_spacer
        self.display_message("Standings:", y = section_y, font = 40)
        self.display_message("Team 0 has {0} points".format(self.game.points[0]), font_color = self.team_colors[0], y = child1_y, font = 34)
        self.display_message("Team 1 has {0} points".format(self.game.points[1]), font_color = self.team_colors[1], y = child2_y, font = 34)

        section_y = child2_y + section_spacer
        child1_y = section_y + parent_child_spacer
        child2_y = child1_y + child_spacer
        self.display_message("Objectives:", y = section_y, font = 40)
        self.display_message("Team 0: "+ self.game.win_conditions[0].description, font_color = self.team_colors[0], y = child1_y, font = 26)
        self.display_message("Team 1: "+ self.game.win_conditions[1].description, font_color = self.team_colors[1], y = child2_y, font = 26)

        section_y = child2_y + section_spacer
        self.display_message("Current Player:", y = section_y, font = 40)

        section_y = section_y + parent_child_spacer + section_spacer
        self.display_message("Instructions:", y = section_y, font = 40)

        section_y = section_y + parent_child_spacer + section_spacer
        self.display_message("Status Messages:", y = section_y, font = 40)

        self.display_screen()


    def display_status(self, text):
        self.display_message(text, 510, font=26, erase=True)
        self.display_screen()

    def display_instruction(self, text):
        self.display_message(text, y=425, font=26, erase=True)
        self.display_screen()

    def display_message(self, message, y = 425, font = 20, font_color = (255,255,255), background_color=(0,0,0), x=None, erase=False):
        if x is None:
            x = int(self.board_width + self.board_x + 10)
        if erase:
            section_spacer = 50
            pygame.draw.rect(self.screen, background_color, pygame.Rect(x, y, self.screen_width, int(section_spacer*0.7)))
        font = pygame.font.Font(None, font)
        message = font.render(message, True, font_color, background_color)
        self.screen.blit(message, (x, y))

    def display_player(self, player):
        for i in range(len(player.hand.cards)):
            card_image = self.image_library[player.hand.cards[i].image_file]
            self.screen.blit(card_image, (self.hand_x + i*self.card_width, self.hand_y))
        self.display_message(player.name, font_color = self.team_colors[player.team_num], y = 325, font = 36)
        self.display_screen()

    def display_screen(self):
        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def wait_for_click(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    return

    def get_card_selection(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    on_board, on_hand, on_deck, coord = self.translate_coord(x, y)
                    if on_board or on_hand or on_deck:
                        return on_board, on_hand, on_deck, coord

    def translate_coord(self, x, y):
        board_i, board_j = (x-self.board_x)//self.card_width, (y-self.board_y)//self.card_height
        hand_i, hand_j = (x-self.hand_x)//self.card_width, (y-self.hand_y)//self.card_height
        deck_i, deck_j = (x-self.deck_x)//int(self.card_width+self.deck_width), (y-self.deck_y)//self.card_height
        on_board, on_hand, on_deck, coord = False, False, False, None
        if 0<=board_i<self.board.size and 0<=board_j<self.board.size:
            on_board = True
            coord = (board_i, board_j)
        elif 0 <= hand_i <= hand_size and 0 <= hand_j <= 1:
            on_hand = True
            coord = hand_i
        elif 0 <= deck_i <= 1 and 0 <= deck_j <= 1:
            on_deck = True
        return on_board, on_hand, on_deck, coord
