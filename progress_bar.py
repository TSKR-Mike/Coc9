import math

import pygame
import pygwidgets
import pyghelpers
import sys
import time
import random
import threading
from math import sin, cos, pi

from typing import Tuple


class windows_progress_bar:
    class _updater(threading.Thread):
        def __init__(self, object, undefined=False):
            super().__init__()
            self.object = object
            self.stop = False
            self.undefined = undefined

        def run(self):
            if self.undefined:
                while self.object.excuted_items < self.object.max_num:
                    if not self.stop:
                        time.sleep(0.05)
                        self.object.undefinded_lenth_update()
            else:
                while self.object.excuted_items < self.object.max_num:
                    if not self.stop:
                        time.sleep(0.05)
                        self.object.update()

        def pause_show(self):
            self.stop = True

        def continue_show(self):
            self.stop = False

    def __init__(self, max_num_of_items: float, window, x=0, y=0, title='progressing...', undefined_lenth=False, item_name='item', specific=True):
        self.last_start_time = None
        self.old_persent_value = 0
        self.window = window
        self.clock = pygame.time.Clock()
        self.max_num = max_num_of_items
        self.title_text = title
        self.step = 0
        self.same_num = 0
        self.last_excuteds = 0
        self.x = x
        self.y = y
        self.item_name = item_name
        self.start_time = 0.0
        self.end_time = 0.0
        self.excuted_items = 0
        self.speed_text = "0.0"
        self.eta_text = '--:--'
        self.last_update_time = None
        self.specific = specific
        self.title = pygwidgets.DisplayText(self.window, (self.x + 55, self.y + 20), self.title_text,
                                            textColor=(0, 0, 0), backgroundColor=pygwidgets.PYGWIDGETS_GRAY,
                                            fontSize=30)
        self.last_EXCUTED_ITEMS = 0
        self.waiting_frame=0
        self.update_time(self.excuted_items)
        self.undefined = undefined_lenth
        self.bkground = pygwidgets.TextButton(self.window,(self.x-5, self.y), "", upColor=pygwidgets.PYGWIDGETS_GRAY
                                              , downColor=pygwidgets.PYGWIDGETS_GRAY, overColor=pygwidgets.PYGWIDGETS_GRAY, height=200, width=606)

    def update(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.excuted_items >= self.max_num:
                        pygame.quit()
                        sys.exit(0)
        except:pass

        if self.last_update_time is None:
            update_time_percent = 1.0 # proportion of updates from 30 frames per sec
            self.last_update_time = time.time()
        else:
            update_time_percent = (time.time() - self.last_update_time) / 0.0333
            self.last_update_time = time.time()

        excuted_items = self.excuted_items
        self.end_time = time.time()
        step = self.step
        window = self.window

        percent_value = round((excuted_items / self.max_num) * 100, 1)
        percent_text = str(round(percent_value)) + '%' + ('      finished ' + str(excuted_items) + 'items in ' + str(
            self.max_num) if self.specific else '')
        percent = pygwidgets.DisplayText(window, (self.x + 70, self.y + 70), percent_text, textColor=(0, 0, 0),
                                         backgroundColor=pygwidgets.PYGWIDGETS_GRAY, fontSize=30,
                                         fontName='TimesNewRoman')

        self.speed = pygwidgets.DisplayText(window, (self.x + 70, self.y + 100),
                                            str(self.speed_text) + self.item_name+'/s', textColor=(0, 0, 0),
                                            backgroundColor=pygwidgets.PYGWIDGETS_GRAY, fontSize=30,
                                            fontName='TimesNewRoman')
        self.eta = pygwidgets.DisplayText(window, (self.x + 370, (self.y + 100) if self.specific else (self.y + 70)), 'ETA:' + self.eta_text,
                                          textColor=(0, 0, 0),
                                          backgroundColor=pygwidgets.PYGWIDGETS_GRAY, fontSize=30,
                                          fontName='TimesNewRoman')
        self.bkground.draw()
        pygame.draw.rect(window, (192, 192, 192), (self.x + 55, self.y + 50, 490, 20))
        pygame.draw.rect(window, (49, 139, 87), (self.x + 55, self.y + 50, percent_value * 4.9, 20))
        # 渐变色的绘制
        pygame.draw.rect(window, (255, 255, 255), (self.x + step + 23, self.y + 50, 10, 20))
        pygame.draw.rect(window, (225, 250, 225), (self.x + step + 33, self.y + 50, 5, 20))
        pygame.draw.rect(window, (180, 250, 190), (self.x + step + 38, self.y + 50, 2, 20))
        pygame.draw.rect(window, (150, 250, 160), (self.x + step + 40, self.y + 50, 2, 20))
        pygame.draw.rect(window, (130, 230, 140), (self.x + step + 42, self.y + 50, 2, 20))
        pygame.draw.rect(window, (110, 210, 130), (self.x + step + 44, self.y + 50, 2, 20))
        pygame.draw.rect(window, (90, 200, 110), (self.x + step + 46, self.y + 50, 2, 20))
        pygame.draw.rect(window, (70, 180, 100), (self.x + step + 48, self.y + 50, 2, 20))
        pygame.draw.rect(window, (60, 160, 90), (self.x + step + 50, self.y + 50, 2, 20))

        pygame.draw.rect(window, (225, 250, 225), (self.x + step + 18, self.y + 50, 5, 20))
        pygame.draw.rect(window, (180, 250, 190), (self.x + step + 16, self.y + 50, 2, 20))
        pygame.draw.rect(window, (150, 250, 160), (self.x + step + 14, self.y + 50, 2, 20))
        pygame.draw.rect(window, (130, 230, 140), (self.x + step + 12, self.y + 50, 2, 20))
        pygame.draw.rect(window, (110, 210, 130), (self.x + step + 10, self.y + 50, 2, 20))
        pygame.draw.rect(window, (90, 200, 110), (self.x + step + 8, self.y + 50, 2, 20))
        pygame.draw.rect(window, (70, 180, 100), (self.x + step + 6, self.y + 50, 2, 20))
        pygame.draw.rect(window, (60, 160, 90), (self.x + step + 4, self.y + 50, 2, 20))
        pygame.draw.rect(window, (192, 192, 192),
                         (self.x + 55 + 4.9 * percent_value, self.y + 50, 490 - 4.9 * percent_value, 20))

        pygame.draw.rect(window, pygwidgets.PYGWIDGETS_GRAY, (self.x, self.y + 50, 55, 20))
        pygame.draw.rect(window, pygwidgets.PYGWIDGETS_GRAY, (self.x + 540, self.y + 50, 60, 20))
        percent.draw()
        self.title.draw()
        speed = (percent_value - self.old_persent_value) * update_time_percent
        if self.waiting_frame == 0:
            if speed * 10 > 5:
                self.step += speed * 10 * update_time_percent
            else:
                self.step += 5 * update_time_percent
        else:
            self.waiting_frame -= 1
        if self.step - 46 >= percent_value * 4.9:
            self.step = 0
            self.waiting_frame = 40
        self.eta.draw()
        if self.specific:
            self.speed.draw()
        pygame.display.update()
        for _ in pygame.event.get():
            pass
        self.old_persent_value = percent_value
        self.last_excuteds = excuted_items
        self.last_start_time = self.start_time

    def undefinded_lenth_update(self):
        step = self.step
        window = self.window
        pygame.draw.rect(window, pygwidgets.PYGWIDGETS_GRAY, (self.x, self.y, 600, 200))
        pygame.draw.rect(window, (192, 192, 192), (self.x + 55, self.y + 50, 490, 20))

        pygame.draw.rect(window, (49, 139, 87), (self.x + 55 + step, self.y + 50, 60, 20))

        pygame.draw.rect(window, pygwidgets.PYGWIDGETS_GRAY, (self.x, self.y + 50, 55, 20))
        pygame.draw.rect(window, pygwidgets.PYGWIDGETS_GRAY, (self.x + 540, self.y + 50, 60, 20))

        self.title.draw()
        self.step += 30
        if self.step - 20 >= 490:
            self.step = 0
        self.clock.tick(30)
        pygame.display.update()
        for _ in pygame.event.get():
            pass

    def update_time(self, num: int):
        if num >= 0 and type(num) == int:
            self.last_EXCUTED_ITEMS = self.excuted_items
            self.excuted_items = num
        self.end_time = time.time()
        if self.last_EXCUTED_ITEMS != self.excuted_items:
            if self.end_time - self.start_time != 0:
                self.same_num = 0
                self.speed_text = str(round((self.excuted_items-self.last_EXCUTED_ITEMS) / (self.end_time - self.start_time), 1))
        else:
            self.same_num += 1
            if self.same_num >= 100:
                self.speed_text = '0.0'
                self.same_num = 0
        if float(self.speed_text) != 0:
            if (round(self.max_num - self.excuted_items) / float(self.speed_text)) < 60:
                if len(str(round((self.max_num - self.excuted_items) / float(self.speed_text)))) == 2:
                    self.eta_text = '00:' + str(math.ceil((self.max_num - self.excuted_items) / float(self.speed_text)))
                else:
                    self.eta_text = '00:0' + str(math.ceil((self.max_num - self.excuted_items) / float(self.speed_text)))
            else:
                self.eta_text = str(
                    round(round(self.max_num - self.excuted_items) / float(self.speed_text)) // 60) + ':' + str(
                    round(math.ceil(self.max_num - self.excuted_items) / float(self.speed_text) % 60 / 12) * 5)
        else:
            self.eta_text = '??:??'
        self.start_time = time.time()

    def show(self):
        self.updater = windows_progress_bar._updater(self, self.undefined)
        self.updater.start()

    def pause(self):
        self.updater.pause_show()

    def continue_draw(self):
        self.updater.continue_show()


class defined_length_initialization_progress_bar:
    class _updater(threading.Thread):
        def __init__(self, object):
            super().__init__()
            self.object = object
            self.quit = False

        def run(self):
            while not self.quit:
                time.sleep(0.05)
                self.object.update()

        def quit_(self):
            self.quit = True

    def __init__(self, radius: int, loc: tuple[int, int], window, total: int, colour: tuple[int, int, int] = (0, 191, 255),
                 bkgcolour: tuple[int, int, int] = (255, 255, 255), width: int = 10, move: bool = True):
        self.updater = None
        self.radius = radius
        self.loc = loc
        self.colour = colour
        self.window = window
        self.bkgcolour = bkgcolour
        self.width = width
        self.length = 1  # angle
        self.start_pos = 0  # angle
        self.end_pos = 0  # angle
        self.circle_num = 0
        self.clock = pygame.time.Clock()
        self.move = move
        self.proceed = 0
        self.total = total

    def update(self):
        self.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        self.percent = round(100 * (self.proceed / self.total), 2)
        self.start_pos %= 360
        self.end_pos %= 360
        if self.move:
            self.start_pos += 0.25
        self.end_pos = self.start_pos + self.percent * 0.0677 * (103/110)
        self.start_pos %= 360
        self.end_pos %= 360
        self.draw()
        self.clock.tick(30)
        for _ in pygame.event.get():
            pass

    def update_items(self, item_proceed: int):
        self.proceed = item_proceed

    def done(self):
        self.updater.quit_()

    def draw(self):
        pygame.draw.arc(self.window, self.colour,
                        (self.loc[0] - self.radius, self.loc[1] - self.radius, self.radius * 2, self.radius * 2),
                        self.start_pos, self.end_pos, width=self.width)
        pygame.display.update()

    def clear(self):
        pygame.draw.arc(self.window, self.bkgcolour,
                        (self.loc[0] - self.radius, self.loc[1] - self.radius, self.radius * 2, self.radius * 2),
                        self.start_pos, self.end_pos, width=self.width)
        pygame.display.update()
        # over drawing the last arc with the bkgcolour

    def run(self):
        self.updater = initialization_progress_bar._updater(object=self)
        self.updater.start()


class initialization_progress_bar:
    class _updater(threading.Thread):
        def __init__(self, object):
            super().__init__()
            self.object = object
            self.quit = False

        def run(self):
            while not self.quit:
                time.sleep(0.05)
                self.object.update()

        def quit_(self):
            self.quit = True

    def __init__(self, radius: int, loc: tuple[int, int], window, colour: tuple[int, int, int] = (0, 191, 255),
                 bkgcolour: tuple[int, int, int] = (255, 255, 255), width: int = 10):
        self.updater = None
        self.radius = radius
        self.loc = loc
        self.colour = colour
        self.window = window
        self.bkgcolour = bkgcolour
        self.width = width
        self.length = 1  # angle
        self.start_pos = 0  # angle
        self.end_pos = 0  # angle
        self.circle_num = 0
        self.clock = pygame.time.Clock()

    def update(self):
        self.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        self.start_pos %= 360
        self.end_pos %= 360
        if self.circle_num <= 20:
            # adding length
            self.length += 0.25
            self.start_pos += 0.15
            self.end_pos = self.start_pos + self.length
        elif self.circle_num <= 40:
            time.sleep(0.01)
            self.length -= 0.25
            self.end_pos += 0.4
            self.start_pos = self.end_pos - self.length
        self.circle_num += 1
        self.circle_num %= 41
        self.circle_num += 1
        self.draw()
        self.clock.tick(30)
        for _ in pygame.event.get():
            pass


    def done(self):
        self.updater.quit_()

    def draw(self):
        pygame.draw.arc(self.window, self.colour,
                        (self.loc[0] - self.radius, self.loc[1] - self.radius, self.radius * 2, self.radius * 2),
                        self.start_pos, self.end_pos, width=self.width)
        pygame.display.update()

    def clear(self):
        pygame.draw.arc(self.window, self.bkgcolour,
                        (self.loc[0] - self.radius, self.loc[1] - self.radius, self.radius * 2, self.radius * 2),
                        self.start_pos, self.end_pos, width=self.width)
        pygame.display.update()
        # over drawing the last arc with the bkgcolour

    def run(self):
        self.updater = initialization_progress_bar._updater(object=self)
        self.updater.start()


class Dot:
    """
    don't add "clock.tick(<any int>)" in the main cycle
    """
    def __init__(self, window, clock, loc, radius, dot_size, dot_colour=(255, 255, 255)):
        self.window, self.loc, self.radius, self.dot_size, self.clock = window, loc, radius, dot_size, clock
        self.theta = 0
        self.dot_colour = dot_colour
        self.drawing = True
        self.waiting_time = 0

    def draw(self, ticking=True):
        if (self.theta % 360) <= 30:
            curr_speed = 4
        elif (self.theta % 360) <= 70:
            curr_speed = 6
        elif (self.theta % 360) <= 108:
            curr_speed = 9
        elif (self.theta % 360) <= 252:
            curr_speed = 12
        elif (self.theta % 360) <= 290:
            curr_speed = 9
        elif (self.theta % 360) <= 330:
            curr_speed = 6
        else:
            curr_speed = 4
        if self.drawing:
            self.theta += curr_speed
            pygame.draw.circle(self.window, self.dot_colour, (
                self.loc[0] + cos((self.theta - 90) * pi / 180) * self.radius,
                self.loc[1] + sin((self.theta - 90) * pi / 180) * self.radius), self.dot_size)
        else:
            self.waiting_time += 1

        if self.waiting_time >= 45:# 60 frames -> 2 secs disappearing
            self.drawing = True
            self.waiting_time = 0

        if self.theta > 720 and self.drawing:
            self.waiting_time = 0
            self.drawing = False
        self.theta %= 720
        if ticking:
            self.clock.tick(30)


class DotCircledProgressBar:
    class _updater(threading.Thread):
        def __init__(self, object):
            super().__init__()
            self.object = object
            self.quit = False

        def run(self):
            while not self.quit:
                self.object.draw()

        def quit_(self):
            self.quit = True

    def __init__(self, window, clock, loc, radius, dot_size, bkg_colour: tuple[int, int, int],
                 dot_colour: tuple[int, int, int] = (255, 255, 255)):
        self.window, self.loc, self.radius, self.dot_size, self.clock = window, loc, radius, dot_size, clock
        self.bkg_colour, self.dot_colour = bkg_colour, dot_colour
        self.dots = [Dot(window, clock, loc, radius, dot_size, dot_colour) for i in range(5)]
        self.drawing_single = 0

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        self.clear()
        if self.drawing_single <= 25:
            self.drawing_single += 1
        self.dots[0].draw()
        if self.drawing_single > 6:
            self.dots[1].draw(ticking=False)
        if self.drawing_single > 12:
            self.dots[2].draw(ticking=False)
        if self.drawing_single > 18:
            self.dots[3].draw(ticking=False)
        if self.drawing_single > 24:
            self.dots[4].draw(ticking=False)
        pygame.display.update()

    def clear(self):
        pygame.draw.arc(self.window, self.bkg_colour,
                        (self.loc[0] - self.radius - self.dot_size*2, self.loc[1] - self.radius - self.dot_size*2,
                         self.radius * 2 + self.dot_size*4, self.radius * 2 + self.dot_size*4),
                        0, 2*pi, width=self.dot_size*4)
        # over drawing the last arc with the bkgcolour

    def run(self):
        self.updater = DotCircledProgressBar._updater(object=self)
        self.updater.start()

    def done(self):
        self.updater.quit_()

if __name__ == '__main__':
    window = pygame.display.set_mode((1004, 600))
    clock = pygame.time.Clock()
    window.fill((0, 191, 255))
    #e = DotCircledProgressBar(window, clock, (400, 300), 40, 5, (0, 191, 255))
    r = windows_progress_bar(1000, window, 200, 200, 'progressing...', undefined_lenth=False, specific=False)
    r.show()
    #e.run()
    #time.sleep(30)
    #e.done()
    #progress = windows_progress_bar(1000, window, 100, 200, undefined_lenth=False)
    k = 0
    #progress.show()
    while k <= 1000:
        #progress.start()
        #time.sleep(0.05)
        k += 1
        #progress.update_time(k)
        r.update_time(k)
        r.update()
