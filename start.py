from sys import exit
from settings import Settings
from time import sleep
from startScreen import start_Screen
from createAlert import create_Alert
from creatWatchlist import create_Watchlist
import pygame as pg

class Start:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        pg.display.set_caption("STOCK ALERTER")

    def draw(self):
        self.screen.fill(self.bg_color)
        pg.display.flip()

    def end_application(self):
      print('\nTerminating\n')
      exit()

value = False
def main():
    application = Start()
    ss = start_Screen(start=application)
    ss.show()

    ca = create_Alert(start=application)  # to prepare start_sc display
    wl = create_Watchlist(start=application)  # to repare watch_List display

    if(ss.alert_btn_click == True):
        ca.show()
        if ca.create_Alert_finished == True:
            main()
    if(ss.watchlist_btn_click == True):
        wl.show_Watchlist()
        if(wl.back_btn_click):
            main()

if __name__ == '__main__':
    main()