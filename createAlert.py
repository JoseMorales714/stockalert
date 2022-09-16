import string
import sys
import pygame as pg
import pygame.event
import pygame_gui
from settings import Settings
import pickle

# Allow user to input stocks. There will be a 5 stock limit


class create_Alert:
    def __init__(self, start):
        self.screen = start.screen
        self.create_Alert_finished = False
        self.alert_list = set()  # An empty list will be made to hold the tickers
        try:
            with open('watchlist.txt', 'rb') as fh:
                self.alert_list = pickle.load(fh)
        except FileNotFoundError:
            print('File not found')

    def show(self):
        w = 900
        h = 900
        CLOCK = pygame.time.Clock()
        refresh_rate = CLOCK.tick(30)
        Manager = pygame_gui.UIManager((w, h))
        input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 50), (150, 40)), manager=Manager,
                                                    object_id="#main_text_entry")
        input.set_text('enter ticker here')
        input.set_allowed_characters(list(map(str, string.ascii_letters)))  # only allow alphabet
        font = pygame.font.Font(None, 32)
        # text = font.render('Enter stock ticker:', (0, 0, 0), False)
        # textRect = text.get_rect()
        # textRect.center = (105, 70)

        
        # to send an email, we can have a bool and if its true it will send the email
        # this conditional statemnet for the bool can be inside the while True block
        # however, we still need the user's email so we'll have to get user input in GUI form
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                    self.add_list(event.text)
                    print(self.get_list())
                    input.set_text('')
                Manager.process_events(event)
            Manager.update(refresh_rate/10000)
            self.screen.fill('blue')
            Manager.draw_ui(self.screen)
            # self.screen.blit(text, textRect)
            pygame.display.update()

    # return the tickers the user wants
    def get_list(self):
        return self.alert_list

    # add a ticker to the list, with a limit of 5
    def add_list(self, tckr):
        if len(self.alert_list) < 5:
            self.alert_list.add(str.upper(tckr))
            with open('watchlist.txt', 'wb') as fh:
                pickle.dump(self.alert_list, fh)
                print('file saved')
        else:
            print('capacity has been reached')

    def return_tickers_list(self):
        return self.alert_list







