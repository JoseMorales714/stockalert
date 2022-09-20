import sys
import pygame as pg
import pygame.event
import pygame_gui
from button import Button
from startScreen import start_Screen

BLACK = (0, 0, 0)


def get_font(size):
    return pygame.font.Font(None, size)


class create_Watchlist:
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
                pygame.quit()
                exit()
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                self.add_list(event.text)
                print(self.get_list())
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.mouse_on_back():
                    self.back_btn_click = True
                    self.create_Watchlist_page_finished = True

        ## the rest of the code below should be arranged in draw()
        w = 700
        h = 700
        CLOCK = pygame.time.Clock()
        refresh_rate = CLOCK.tick(30)
        Manager = pygame_gui.UIManager((w, h))
        input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 10), (80, 40)), manager=Manager,

                                                 object_id="#main_text_entry")



                Manager.process_events(event)
            Manager.update(refresh_rate/10000)
            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            Manager.draw_ui(self.screen)
            PLAY_TEXT = get_font(160).render("Watchlist", True, "Green")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 100))
            self.screen.blit(PLAY_TEXT, PLAY_RECT)

    def draw(self):
        self.screen.fill(BLACK)
        self.back_btn.draw()

        pg.display.flip()

    def show(self):
        while not self.create_Watchlist_page_finished:
            self.draw()
            self.check_events()


            ##pygame.display.update()











