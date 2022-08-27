from sys import exit
from settings import Settings
from time import sleep
from startScreen import start_Screen
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

def main():
    application = Start()
    ss = start_Screen(start=application)
    ss.show()

    # second =

if __name__ == '__main__':
    main()
