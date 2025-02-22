import pygame
import sys


class VerticalScroller:
    def __init__(self, window, x, y, height, width, total_height, bar_colour=(155,155,155), bkg_colour=(199,199,199)):
        self.x, self.y, self.width, self.height, self.total_height, self.bar_colour, self.bkg_colour = x, y, width, height, total_height, bar_colour,bkg_colour
        self.window = window
        self.scroller_y = 0
        self.is_dragging = False
        self.clicked_point = 0

    def draw(self):
        pygame.draw.rect(self.window, self.bkg_colour, (self.x, self.y, self.width, self.total_height))
        pygame.draw.rect(self.window, self.bar_colour, (self.x, self.scroller_y + self.y, self.width, self.height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x + self.width >= event.pos[0] >= self.x and self.scroller_y + self.height + self.y >= event.pos[1] >= self.scroller_y + self.y:
                self.is_dragging = True
                self.clicked_point = event.pos[1] - self.y - self.scroller_y
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
            self.clicked_point = 0
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                if self.total_height + self.y + self.clicked_point - self.height >= event.pos[1] >= self.y + self.clicked_point:
                    self.scroller_y = event.pos[1] - self.y - self.clicked_point
                else:
                    if event.pos[1] < self.y + self.clicked_point:
                        self.scroller_y = 0
                    else:
                        self.scroller_y = self.total_height - self.height


class HorizontalScroller:
    def __init__(self, window, x, y, height, width, total_width, bar_colour=(155, 155, 155),
                 bkg_colour=(199, 199, 199)):
        self.x, self.y, self.width, self.height, self.total_width, self.bar_colour, self.bkg_colour = x, y, width, height, total_width, bar_colour, bkg_colour
        self.window = window
        self.scroller_x = 0
        self.is_dragging = False
        self.clicked_point = 0

    def draw(self):
        pygame.draw.rect(self.window, self.bkg_colour, (self.x, self.y, self.total_width, self.height))
        pygame.draw.rect(self.window, self.bar_colour, (self.x + self.scroller_x, self.y, self.width, self.height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.width + self.scroller_x + self.x + self.width >= event.pos[0] >= self.scroller_x + self.x and self.height + self.y >= event.pos[
                1] >= self.y:
                self.is_dragging = True
                self.clicked_point = event.pos[0] - self.x - self.scroller_x
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
            self.clicked_point = 0
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                if self.total_width + self.x + self.clicked_point - self.width >= event.pos[0] >= self.x + self.clicked_point:
                    self.scroller_x = event.pos[0] - self.x - self.clicked_point
                else:
                    if event.pos[0] < self.x + self.clicked_point:
                        self.scroller_x = 0
                    else:
                        self.scroller_x = self.total_width - self.width

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    a = VerticalScroller(window, 580, 0, 40, 20, 400)
    b = HorizontalScroller(window, 0, 380, 20, 90, 580)
    while True:
        for event in pygame.event.get():
            window.fill((0, 191, 255))
            a.draw()
            a.handle_event(event)
            b.draw()
            b.handle_event(event)

            pygame.display.update()
            clock.tick(30)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

