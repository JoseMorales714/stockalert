import sys
import pygame as pg
import pygame.event
import pygame_gui
from button import Button
from createAlert import alert_list
# from start import Start
from startScreen import start_Screen
import yfinance as yf


def get_font(size):
    return pygame.font.Font(None, size)


class create_Watchlist():
    def __init__(self, start):
        self.screen = start.screen
        self.create_Watchlist_page_finished = False

    def show(self):
        bg = pg.image.load("createwatchlist.png")
        bg = pg.transform.scale(bg,(1200, 600))
        w = 1200
        h = 800
        CLOCK = pygame.time.Clock()
        PLAY_TEXT = get_font(120).render("Watchlist", True, "Green")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(600, 100))
        refresh_rate = CLOCK.tick(30)
        Manager = pygame_gui.UIManager((w, h), 'theme.json')
        click = pg.mixer.Sound("mixkit-classic-click-1117.wav") #adds sound



       #BUTTONS
        pygame_gui.elements.UIButton(text='Back', manager=Manager, relative_rect=pygame.Rect(35, 10, 100, 50),
                                     object_id='#back')
        pygame_gui.elements.UIButton(text='Clear', manager=Manager, relative_rect=pygame.Rect(1000,520,100,50),
                                     object_id='clear')


        while not self.create_Watchlist_page_finished:
            display_list = []  # will contain the renders for each tckr
            #for i in alert_list:  # for every tckr

                #pg.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                    self.add_list(event.text)
                    print(self.get_list())
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == '#back':
                      pg.mixer.Sound.play(click)
                      pg.mixer.music.stop()
                      self.create_Watchlist_page_finished = True
                    if event.ui_object_id == 'clear':
                        pg.mixer.Sound.play(click)
                        pg.mixer.music.stop()
                        open('watchlist.txt','w').close()

                Manager.process_events(event)
            Manager.update(refresh_rate / 10000)
            self.screen.blit(bg, (0,0))
            Manager.draw_ui(self.screen)
            pygame.display.set_caption("Watchlist")
            Icon = pygame.image.load("watchlist.svg.png")
            pygame.display.set_icon(Icon)
            self.screen.blit(PLAY_TEXT, PLAY_RECT)
            for i in alert_list:
                ticker = yf.Ticker(str(i))
                price = str(ticker.info['regularMarketPrice'])
                PLAY_TEXT1 = get_font(90).render('$' + str(i) + ' ' + price, True, "White")  # create a render
                display_list.append(PLAY_TEXT1)
            y = 200
            for d in display_list:  # for every render in display_list
                self.screen.blit(d, PLAY_TEXT1.get_rect(center=(600, y)))  # blit
                y += 100  # so that the next rect is lower on the screen
            pygame.display.update()







