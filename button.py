import pygame.font
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
class Button:
    def __init__(self, screen, msg, ul):
        self.screen = screen
        self.width, self.height = 220, 50
        self.colors = [BLACK, RED]
        self.color_id = 0
        self.color = self.colors[self.color_id]
        self.color = GREEN
        self.text_color = WHITE
        self.font = pygame.font.SysFont(None, 48)
        self.ul = ul

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left, self.rect.top = ul[0], ul[1]

        self.msg = msg
        self.image = self.font.render(self.msg, True, self.text_color, self.color)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

    def draw(self):
        color = self.colors[self.color_id]
        self.image = self.font.render(self.msg, True, self.text_color, color)
        self.screen.fill(color, self.rect)
        self.screen.blit(self.image, self.image_rect)