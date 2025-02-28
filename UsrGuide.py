import pygame
import sys
from matrix import subWindow
from CoordinateSystem import Button

class UsrNotice(subWindow):

    def __init__(self, window, loc, length, height, bkg_colour=(0, 191, 255), title='User Guide'):
        super().__init__(window, loc, length, height, bkg_colour=bkg_colour, title=title)
        self.font = pygame.font.Font('fonts/JetBrainsMono-Light.ttf')
        self.texts_p1 = []
        self.texts_p2 = []

        self.texts_p1.append(
            self.font.render('                                Common Questions(P1)', True,
                             (0, 0, 0)))
        self.texts_p1.append(self.font.render('1. About root', True, (0, 0, 0)))
        self.texts_p1.append(
            self.font.render('     To use "root", you need to type the number of root BEFORE the "root" symbol,',
                             True, (0, 0, 0)))
        self.texts_p1.append(self.font.render('     like "2√4" means ²√4, instead of 2*²√4',
                                              True, (150, 0, 0)))
        self.texts_p1.append(self.font.render('2. Why is the window stuck?', True, (0, 0, 0)))
        self.texts_p1.append(
            self.font.render('     Minimize all windows to look for unclosed warning/question/error windows',
                             True, (0, 0, 0)))
        self.texts_p1.append(self.font.render('     , this will lead to the stuck of main loop.', True, (0, 0, 0)))
        self.texts_p1.append(self.font.render('     (the windows will NOT show up in the quick bar)', True, (150, 0, 0)))
        self.texts_p1.append(self.font.render('3. About "No-mouse" mode', True, (0, 0, 0)))
        self.texts_p1.append(
            self.font.render('     The No-mouse mode is designed of the users who do NOT have mouse or keyboards', True,
                             (0, 0, 0)))
        self.texts_p1.append(
            self.font.render('     so that they can better interact with charts in "complex" and "vector".', True,
                             (0, 0, 0)))
        self.texts_p1.append(self.font.render('     If you have mouse and keyboard, you can ignore it.', True, (0, 0, 0)))
        self.texts_p1.append(self.font.render('4. How to use matrix/complex/vector', True, (0, 0, 0)))
        self.texts_p1.append(
            self.font.render('     Usually, select a file to insert data from it.You can find them in ',
                             True, (0, 0, 0)))
        self.texts_p1.append(
            self.font.render('     /Coc<Type>Files or input the data manually and extract them later.',
                             True, (0, 0, 0)))
        self.texts_p1.append(
            self.font.render('      The interact guide is on the the title bar.',
                             True, (0, 0, 0)))
        self.texts_p1.append(self.font.render('5. How to insert data from Excel files', True, (0, 0, 0)))
        self.texts_p1.append(self.font.render('     There is guide about how to load data in data science functions and matrix.', True, (0, 0, 0)))
        self.texts_p1.append(
            self.font.render('     Follow the guide there.', True,
                             (0, 0, 0)))

        self.texts_p2.append(
            self.font.render('                                Common Questions(P2)', True,
                             (0, 0, 0)))
        self.texts_p2.append(
            self.font.render('6.How to copy the answer/formula', True,
                             (0, 0, 0)))
        self.texts_p2.append(
            self.font.render('     For formula, press the "copy formula" button. As for the answer, use Ctrl+C or ', True,
                             (0, 0, 0)))
        self.texts_p2.append(
            self.font.render('     click the button "copy answer".', True,
                             (0, 0, 0)))
        self.texts_p2.append(
            self.font.render('7.Compound expression', True,
                             (0, 0, 0)))
        self.texts_p2.append(
            self.font.render('     Most of the functions is available with compound expressions.', True,
                             (0, 0, 0)))
        self.texts_p2.append(
            self.font.render('     But the base of Log (mean the "n" part of "nlogm") do NOT support operations', True,
                             (150, 0, 0)))
        self.texts_p2.append(
            self.font.render(
                '     like this.', True,
                (150, 0, 0)))

        self.left = Button(window, (loc[0]+self.length-60, loc[1]+self.height-30), 30, 30, '<',(200, 200, 200),
                                     (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.right = Button(window, (loc[0] + self.length - 30, loc[1] + self.height - 30), 30, 30, '>', (200, 200, 200),
                           (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.page = 0

    def draw(self):
        while True:
            pygame.draw.rect(self.window, self.bkg_colour, (self.loc[0], self.loc[1], self.length, self.height))
            if not self.page == 0:
                self.left.draw()
            if not self.page == 1:
                self.right.draw()
            for event in pygame.event.get():
                if self.cancel_button.handleEvent(event):
                    return
                if self.left.handle_event(event):
                    if self.page != 0:self.page -= 1
                if self.right.handle_event(event):
                    if self.page != 1:self.page += 1
            self.title_bkg.draw()
            self.title_view.draw()
            self.cancel_button.draw()
            if self.page == 0:
                for obj, i in zip(self.texts_p1, range(len(self.texts_p1))):
                    self.window.blit(obj, (0, 30 * i + 30))
            elif self.page == 1:
                for obj, i in zip(self.texts_p2, range(len(self.texts_p2))):
                    self.window.blit(obj, (0, 30 * i + 30))
            pygame.display.update()



if __name__ == '__main__':
    pygame.init()
    screen_width, screen_height = 1004, 610
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Simple Pygame Window")
    a = UsrNotice(screen, (0, 0), 1004, 610)
    a.draw()

    pygame.quit()
    sys.exit()
