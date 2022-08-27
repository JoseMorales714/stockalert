import sys
import pygame as pg
from button import Button


GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (130, 130, 130)

class start_Screen:
    def __init__(self, start):
        self.screen = start.screen
        self.start_Screen_finished = False

        headingFont = pg.font.SysFont(None, 192)
        subheadingFont = pg.font.SysFont(None, 122)

        strings = [('Stock', RED, headingFont), ('Alerter', GREEN, subheadingFont)]

        self.texts = [self.get_text(msg=s[0], color=s[1], font=s[2]) for s in strings]
        self.posns = [150, 250]
        idk = [1000 * x + 400 for x in range(4)]
        self.posns.extend(idk)

        centerx = self.screen.get_rect().centerx
        self.play_button = Button(self.screen, "Create Alert", ul=(centerx - 105 , 400))

        n = len(self.texts)
        # self.rects = [self.get_text_rect(text=self.texts[i], centerx=centerx, centery=self.posns[i]) for i in range(n)]

    def get_text(self, font, msg, color):
        return font.render(msg, True, color, BLACK)

    def get_text_rect(self, text, centerx, centery):
        rect = text.get_rect()
        rect.centerx = centerx
        rect.centery = centery
        return rect

    def mouse_on_button(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        return self.play_button.rect.collidepoint(mouse_x, mouse_y)

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.MOUSEBUTTONDOWN:
                if self.mouse_on_button():
                    self.start_Screen_finished = True
            if e.type == pg.QUIT:
                sys.exit()


    def show(self):
        while not self.start_Screen_finished:
            self.draw()
            self.check_events()  # exits game if QUIT pressed

    def draw_text(self):
        n = len(self.texts)
        for i in range(n):
            self.screen.blit(self.texts[i], self.rects[i])


    def draw(self):
        self.screen.fill(BLACK)
        self.draw_text()
        self.play_button.draw()
        pg.display.flip()