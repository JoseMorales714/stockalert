import string
import sys
import pygame as pg
import pygame.event
import pygame_gui
from mail import create_email
from settings import Settings
import pickle
import yfinance as yf

# TO DO: Maybe make the ticker input box a button at first that tells you to enter a ticker and changes to input box when clicked
# Maybe you dont have to keep using kill to get rid of buttons, use visible instead
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
        self.screen = pg.display.set_mode((1200, 800))
        self.create_Alert_finished = False
        self.haveUser = False

    def show(self):
        bg = pg.transform.scale(pg.image.load("mountains.jpeg"), (1200, 800))

        w = 1200
        h = 800
        CLOCK = pygame.time.Clock()
        refresh_rate = CLOCK.tick(5)
        Manager = pygame_gui.UIManager((w, h), 'theme.json')
        font = pygame.font.Font(None, 36)
        # welcomeText = font.render('Welcome, ' + str(email_address), True, (255, 165, 0), None)
        # welcomeTextRect = welcomeText.get_rect()
        Alert_button = pygame_gui.elements.UIButton(text='Alert', manager=Manager,
                                     relative_rect=pygame.Rect(w / 2 - 50, h / 2 + 20, 100, 40),
                                     object_id='#finished')
        Alert_button.visible = 0
        pygame_gui.elements.UIButton(text='Return', manager=Manager,
                                     relative_rect=pygame.Rect(35, h - 160, 100, 50),
                                     object_id='#back')
        welcomeText = font.render(str.upper('Welcome, ' + str(email_address)), True, (255, 145, 0), None)
        welcomeTextRect = welcomeText.get_rect()
        welcomeTextRect.center = (w / 2, 60)
        Tickerinput = make_ticker_input(w, h, Manager)
        Tickerinput.visible = 0
        Emailinput = make_email_input(w, h, Manager)
        Emailinput.visible = 0
        if email_address != '':
            changeEmail_button = pygame_gui.elements.UIButton(text='change email', manager=Manager,
                                                              relative_rect=pygame.Rect(w - 180, 30, 150, 50),
                                                              object_id='#change')
            print(email_address)
            Tickerinput.visible = 1
        else:
            print('No user')
            Emailinput.visible = 1
        while not self.create_Alert_finished:
            CLOCK.tick(30)

            if Tickerinput.get_text() == '':
                Tickerinput.set_text('Ticker')
            if Tickerinput.is_focused and Tickerinput.get_text() == "Ticker":
                Tickerinput.set_text('')
            if Emailinput.get_text() == '':
                Emailinput.set_text('Email')
            if Emailinput.is_focused and Emailinput.get_text() == "Email":
                Emailinput.set_text('')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == '#finished':
                        alert = create_email()
                        with open('email.txt', 'rb') as fh:
                            e = pickle.load(fh)
                        alert.send_email(user_email=e, stocks=alert_list)
                    if event.ui_object_id == '#back':
                        self.create_Alert_finished = True
                    if event.ui_object_id == "#change":
                        Alert_button.visible = 0 # we dont need alert button. alert list will be empty
                        open('email.txt', 'w').close()
                        open('watchlist.txt', 'w').close()
                        changeEmail_button.kill()
                        Tickerinput.kill()
                        Emailinput = make_email_input(w, h, Manager)
                        welcomeText = font.render(str.upper('Welcome, '), True, (255, 145, 0), None)
                        welcomeTextRect = welcomeText.get_rect()
                        welcomeTextRect.center = (w / 2, 60)
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_object_id == "#username_text_entry":
                        self.get_user(event.text)
                        print(self.get_list())
                        print(email_address)
                        Emailinput.kill()
                        Tickerinput = make_ticker_input(w, h, Manager)
                        Alert_button.visible = 1
                        changeEmail_button = pygame_gui.elements.UIButton(text='change email', manager=Manager,
                                                                          relative_rect=pygame.Rect((w - 180, 30),
                                                                                                    (150, 50)),
                                                                          object_id='#change')
                        try:  # IDK IF THIS SHOULD GO HERE ! IT WORKS BUT SEEMS MESSY CALLING THIS AGAIN
                            with open('email.txt', 'rb') as fh:
                                e = pickle.load(fh)
                        except FileNotFoundError:
                            e = ''
                            print('File email.txt not found ')
                        except EOFError:
                            e = ''
                            print("No input to read")
                        welcomeText = font.render(str.upper('Welcome, ' + str(e)), True, (255, 145, 0), None)
                        welcomeTextRect = welcomeText.get_rect()
                        welcomeTextRect.center = (w / 2, 60)

                    if event.ui_object_id == "#main_text_entry":
                        stock = yf.Ticker(Tickerinput.text)
                        if stock.info['regularMarketPrice'] == None:
                            Tickerinput.set_text("")
                            print("invalid")
                        else:  # valid ticker, add to the list
                            print(Tickerinput.text)
                            if len(alert_list) < 5:
                                alert_list.add(str.upper(Tickerinput.text))
                                with open('watchlist.txt', 'wb') as fh:
                                    pickle.dump(alert_list, fh)
                                    print('watchlist File saved')
                            else:
                                print('capacity has been reached')
                            print(self.get_list())
                            Tickerinput.set_text('')

                Manager.process_events(event)
            Manager.update(refresh_rate / 10000)
            self.screen.blit(bg, (0, 0))
            Manager.draw_ui(self.screen)
            self.screen.blit(welcomeText, welcomeTextRect)
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
    ticker_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(xpos / 2 - 120 / 2, ypos / 2 - 40 / 2, 120, 40),
        manager=manager,
        object_id="#main_text_entry")
    # ticker_input.set_text('Enter Ticker')
    ticker_input.set_allowed_characters(
        list(map(str, string.ascii_letters)))  # only allow alphabet characters for input
    return ticker_input


def make_email_input(xpos, ypos, manager):
    email_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(xpos / 2 - 350 / 2, ypos / 2 - 40 / 2, 350, 40),
        manager=manager,
        object_id="#username_text_entry")
    # email_input.set_text('Enter Email')
    email_input.set_forbidden_characters([' '])  # no spaces allowed
    return email_input


def get_email():  # might need this if i want to clean up some code ?
    try:
        with open('email.txt', 'rb') as fh:
            email_address = pickle.load(fh)
    except FileNotFoundError:
        email_address = ''
        print('File email.txt not found ')
    except EOFError:
        email_address = ''
        print("No input to read")
    return email_address