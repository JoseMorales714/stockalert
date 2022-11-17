import string
import sys
import pygame as pg
import pygame.event
import pygame_gui
from mail import create_email
from settings import Settings
import pickle
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
        self.settings = Settings()
        self.screen = pg.display.set_mode((1200,
                                           800))
        self.create_Alert_finished = False
        # self.alert_list = []  # An empty list will be made to hold the tickers
        self.haveUser = False

    def show(self):
        bg = pg.image.load("mountains.jpeg")
        bg = pg.transform.scale(bg, (1200, 800))

        w = 1200
        h = 800
        CLOCK = pygame.time.Clock()
        refresh_rate = CLOCK.tick(30)
        Manager = pygame_gui.UIManager((w, h), 'theme.json')
        font = pygame.font.Font(None, 26)
        text = font.render('Welcome, ' + str(email_address), (255, 255, 255), False)
        textRect = text.get_rect()
        add_ticker_button = pygame_gui.elements.UIButton(text='Add', manager=Manager,
                                                           relative_rect=pygame.Rect(w/2 - 50, h/2 + 20, 100, 40),
                                                           object_id='#confirm')
        add_ticker_button.disable()
        pygame_gui.elements.UIButton(text='Alert', manager=Manager,
                                                   relative_rect=pygame.Rect(w/2 - 50, h/2 + 60, 100, 40),
                                                   object_id='#finished')
        pygame_gui.elements.UIButton(text='Return', manager=Manager,
                                                   relative_rect=pygame.Rect(35, h - 160, 100, 50),
                                                   object_id='#back')
        if email_address != '':
            changeEmail_button = pygame_gui.elements.UIButton(text='change email', manager=Manager,
                                                              relative_rect=pygame.Rect(w - 180, 30, 150, 50),
                                                              object_id='#change')
            print(email_address)
            input = make_ticker_input(w, h, Manager)
        else:
            print('No user')
            input = make_email_input(w, h, Manager)

        while not self.create_Alert_finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and (event.ui_object_id == "#main_text_entry"):
                    add_ticker_button.enable()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == '#confirm':
                        ticker = yf.Ticker(input.text)
                        if (ticker.info['regularMarketPrice'] == None):
                            raise NameError("You did not input a correct stock ticker! Try again.")
                        else:  #  valid ticker, add to the list
                            print(input.text)
                            if len(alert_list) < 5:
                                alert_list.add(str.upper(input.text))
                                with open('watchlist.txt', 'wb') as fh:
                                    pickle.dump(alert_list, fh)
                                    print('watchlist File saved')
                            else:
                                print('capacity has been reached')
                            print(self.get_list())
                            input.set_text('')
                            add_ticker_button.disable()
                    if event.ui_object_id == '#finished':
                        alert = create_email()
                        alert.send_email(user_email=email_address, stocks=alert_list)
                    if event.ui_object_id == '#back':
                        self.create_Alert_finished = True
                    if event.ui_object_id == "#change":
                        open('email.txt', 'w').close()
                        open('watchlist.txt', 'w').close()
                        changeEmail_button.kill()
                        input.kill()
                        input = make_email_input(w, h, Manager)
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#username_text_entry":
                    self.get_user(event.text)
                    print(self.get_list())
                    print(email_address)
                    input.kill()
                    input = make_ticker_input(w, h, Manager)
                    changeEmail_button = pygame_gui.elements.UIButton(text='change email', manager=Manager,
                                                                      relative_rect=pygame.Rect((w - 180, 30), (150, 50)),
                                                                      object_id='#change')
                Manager.process_events(event)
            Manager.update(refresh_rate / 10000)
            self.screen.blit(bg, (0, 0))
            Manager.draw_ui(self.screen)
            self.screen.blit(text, textRect)
            pygame.display.update()

    # return the tickers the user wants
    def get_list(self):
        return alert_list

    def get_user(self, username):
        self.haveUser = True
        with open('email.txt', 'wb') as fh:
            pickle.dump(username, fh)
            print('user file saved')

        
def make_ticker_input(xpos, ypos, manager):
    ticker_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(xpos / 2 - 150 / 2, ypos / 2 - 40 / 2, 150, 40),
                                        manager=manager,
                                        object_id="#main_text_entry")
    ticker_input.set_text('Enter ticker')
    ticker_input.set_allowed_characters(
        list(map(str, string.ascii_letters)))  # only allow alphabet characters for input
    return ticker_input


def make_email_input(xpos, ypos, manager):
    email_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(xpos / 2 - 350 / 2, ypos / 2 - 40 / 2, 350, 40),
                                                manager=manager,
                                                object_id="#username_text_entry")
    email_input.set_text('enter email')
    email_input.set_forbidden_characters([' '])  # no spaces allowed
    return email_input






