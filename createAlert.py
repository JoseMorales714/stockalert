import string
import sys
import pygame as pg
import pygame.event
import pygame_gui
from mail import create_email
from settings import Settings
import pickle
from button import Button
import yfinance as yf

try:
    with open('watchlist.txt', 'rb') as fh:
        alert_list = pickle.load(fh)
except FileNotFoundError:
    alert_list = set()
    print('File watchlist.txt not found ')
except EOFError:
    alert_list = set()
    print("No input to read")
try:
    with open('email.txt', 'rb') as fh:
        email_address = pickle.load(fh)
except FileNotFoundError:
    email_address = ''
    print('File email.txt not found ')
except EOFError:
    email_address = ''
    print("No input to read")


class create_Alert:
    def __init__(self, start):
        self.screen = start.screen
        self.create_Alert_finished = False
        self.alert_list = []  # An empty list will be made to hold the tickers
        self.haveUser = False

    def show(self):
        w = 900
        h = 900
        CLOCK = pygame.time.Clock()
        refresh_rate = CLOCK.tick(30)
        Manager = pygame_gui.UIManager((w, h))
        font = pygame.font.Font(None, 26)
        text = font.render('Welcome, ' + str(email_address), (0, 0, 0), False)
        textRect = text.get_rect()
        textRect = (10, 20)
        confirmation_button = pygame_gui.elements.UIButton(text='add', manager=Manager,
                                                           relative_rect=pygame.Rect((10, 100), (100, 50)),
                                                           object_id='#confirm')
        confirmation_button.disable()
        done_button = pygame_gui.elements.UIButton(text='alert', manager=Manager,
                                                   relative_rect=pygame.Rect((110, 100), (100, 50)),
                                                   object_id='#finished')
        back_button = pygame_gui.elements.UIButton(text='return', manager=Manager,
                                                   relative_rect=pygame.Rect((110, 150), (100, 50)),
                                                   object_id='#back')
        if email_address != '':
            changeEmail_button = pygame_gui.elements.UIButton(text='change email', manager=Manager,
                                                              relative_rect=pygame.Rect((610, 100), (150, 50)),
                                                              object_id='#change')
            print(email_address)
            input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 50), (150, 40)), manager=Manager,
                                                        object_id="#main_text_entry")
            input.set_text('enter ticker')
            input.set_allowed_characters(
                list(map(str, string.ascii_letters)))  # only allow alphabet characters for input
        else:
            print('No user')
            input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 50), (350, 40)), manager=Manager,
                                                        object_id="#username_text_entry")
            input.set_text('enter email')
            input.set_forbidden_characters([' '])  # no spaces allowed

        while not self.create_Alert_finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and (event.ui_object_id == "#main_text_entry"):
                    confirmation_button.set_text('Add')
                    confirmation_button.enable()
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == '#confirm':
                    ticker = yf.Ticker(input.text)
                    if (ticker.info['regularMarketPrice'] == None):
                        raise NameError("You did not input a correct stock ticker! Try again.")
                    self.add_list(input.text)
                    print(self.get_list())
                    input.set_text('')
                    confirmation_button.disable()
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == '#finished':
                    alert = create_email()
                    alert.send_email(user_email=email_address, stocks=alert_list)
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#back":
                    self.create_Alert_finished = True
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#change":
                    open('email.txt', 'w').close()
                    open('watchlist.txt', 'w').close()
                    changeEmail_button.kill()
                    input.kill()
                    input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 50), (350, 40)),
                                                                manager=Manager,
                                                                object_id="#username_text_entry")
                    input.set_text('enter email')

                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#username_text_entry":
                    self.get_user(event.text)
                    print(self.get_list())
                    print(email_address)
                    input.kill()
                    input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 50), (150, 40)),
                                                                manager=Manager,
                                                                object_id="#main_text_entry")
                    changeEmail_button = pygame_gui.elements.UIButton(text='change email', manager=Manager,
                                                                      relative_rect=pygame.Rect((610, 100), (150, 50)),
                                                                      object_id='#change')
                    input.set_text('enter ticker')
                Manager.process_events(event)
            Manager.update(refresh_rate / 10000)
            self.screen.fill('blue')
            Manager.draw_ui(self.screen)
            self.screen.blit(text, textRect)
            pygame.display.update()

    # return the tickers the user wants
    def get_list(self):
        return alert_list

    # add a ticker to the list, with a limit of 5
    def add_list(self, tckr):
        print(tckr)
        if len(alert_list) < 5:
            alert_list.add(str.upper((tckr)))
            with open('watchlist.txt', 'wb') as fh:
                pickle.dump(alert_list, fh)
                print('watchlist File saved')
        else:
            print('capacity has been reached')

    def get_user(self, username):
        self.haveUser = True
        with open('email.txt', 'wb') as fh:
            pickle.dump(username, fh)
            print('user file saved')







