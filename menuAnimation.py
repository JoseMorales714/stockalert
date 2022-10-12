import pygame as pg
import sys

class menu_Animation(pg.sprite.Sprite):
    def __int__(self, start, x, y):
        self.screen = start.screen
        self.screen_rect = self.screen.get_rect
        super().__init__()
        self.start_animation = False
        self.sprites = []
        self.sprites.append(pg.image.load(f'pics/stockanimate-1.png.png'))
        self.sprites.append(pg.image.load(f'pics/stockanimate-2.png.png'))
        self.sprites.append(pg.image.load(f'pics/stockanimate-3.png.png'))
        self.curr_sprite = 0
        self.image = self.sprites[self.curr_sprite]

        self.rect = self.screen.get_rect()
        self.rect.topleft = [x,y]

    def start(self):
        self.start_animation = False

    def update(self, rate):
        if self.start_animation:
            self.curr_sprite += rate
            if int(self.curr_sprite) >= len(self.sprites):
                self.curr_sprite = 0
                self.start_animation = False
        self.image = self.sprites[int(self.curr_sprite)]