import sys
import pygame as pg
import pygame.event
import pygame_gui
from button import Button
from createAlert import alert_list
# from start import Start
from startScreen import start_Screen
import yfinance as yf

BLACK = (0, 0, 0)


def get_font(size):
    return pygame.font.Font(None, size)


class create_Watchlist():
    def __init__(self, start):
        self.screen = start.screen
        self.create_Watchlist_page_finished = False
        self.back_btn_click = False
        self.back_btn = Button(self.screen, "back", ul=(-10, 60))

    def mouse_on_back(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.back_btn.rect.collidepoint(mouse_x, mouse_y)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                self.add_list(event.text)
                print(self.get_list())
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.mouse_on_back():
                    self.back_btn_click = True
                    self.create_Watchlist_page_finished = True

    def draw(self):
        display_list = []  # will contain the renders for each tckr
        for i in alert_list:  # for every tckr
            ticker = yf.Ticker(str(i))
            price = str(ticker.info['regularMarketPrice'])
            PLAY_TEXT = get_font(90).render('$' + str(i) + ' ' + price, True, "Green")  # create a render
            display_list.append(PLAY_TEXT)  # append it to display_list
        self.screen.fill(BLACK)
        self.back_btn.draw()
        pygame.display.set_caption("Watchlist")
        # Icon = pygame.image.load("watchlist.svg.png")
        # pygame.display.set_icon(Icon)
        # PLAY_TEXT = get_font(120).render("Watchlist", True, "Green")
        # PLAY_RECT = PLAY_TEXT.get_rect(center=(500, 100))
        # self.screen.blit(PLAY_TEXT, PLAY_RECT)
        # PLAY_TEXT = get_font(80).render("apple", True, "red")   # just and idea how it will look
        # PLAY_RECT = PLAY_TEXT.get_rect(center=(200, 180))
        # self.screen.blit(PLAY_TEXT, PLAY_RECT)
        # PLAY_TEXT = get_font(80).render("120", True, "green")  # price
        # PLAY_RECT = PLAY_TEXT.get_rect(center=(350, 180))
        # self.screen.blit(PLAY_TEXT, PLAY_RECT)
        y = 100
        for d in display_list:  # for every render in display_list
            self.screen.blit(d, PLAY_TEXT.get_rect(center=(640, y)))  # blit
            y += 50  # so that the next rect is lower on the screen
        pg.display.flip()

    def show_Watchlist(self):
        while not self.create_Watchlist_page_finished:
            self.draw()
            self.check_events()

            pygame.display.update()
