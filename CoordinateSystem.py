import random
import datetime

import pygame
import pygwidgets
from pygame.locals import *
import math
import numpy as np
from math import pi
from checkbox import CheckBox

pygame.init()
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
from mpl_toolkits.mplot3d import Axes3D

all_colours = ['blue', 'red', 'green', 'purple', 'darkorange', 'magenta', 'brown']
sensitivity = 0.5
POINT, LINE, ARROW = 0, 1, 2
plt.rcParams['lines.antialiased'] = True
plt.rcParams['patch.antialiased'] = True

class CoordinateSystem2d:
    def __init__(self, window, loc, size, title='', x_item_name='X', y_item_name='Y', no_mouse=False, axis_limits: list[int]=None):
        if axis_limits is None:
            axis_limits = (5, 5, -5, -5)
        self.size = size
        self.is_dragging = False
        self.fig = pylab.figure(figsize=(size[0] / 100, size[1] / 100),  # Inches
                                dpi=100)  #dots per inch
        self.title, self.x_item_name, self.y_item_name = title, x_item_name, y_item_name
        self.window, self.loc = window, loc
        self.no_mouse = no_mouse
        self.clock = pygame.time.Clock()
        self.points = []  #(loc, color, texts->None)
        self.lines = []  #(start-loc, end-loc, color, texts->None)
        self.arrows = []  #(start-loc, end-loc, color, texts->None)
        self.coord_x_max, self.coord_y_max, self.coord_x_min, self.coord_y_min = axis_limits
        self.x_length_per_line = (size[0]) / 10
        self.y_length_per_line = (size[1]) / 10
        self.length = size[0]
        self.height = size[1]
        self.num = 0
        self.last_lim = [self.coord_x_min, self.coord_x_max, self.coord_y_min, self.coord_y_max]
        self.left_move_button = Button(self.window, (self.loc[0], self.loc[1] + 30), 30, 30, '<-', (200, 200, 200),
                                       (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.reset_button = Button(self.window, (self.loc[0] + 30, self.loc[1] + 30), 60, 30, 'reset', (200, 200, 200),
                                   (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.right_move_button = Button(self.window, (self.loc[0] + 90, self.loc[1] + 30), 30, 30, '->',
                                        (200, 200, 200), (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf',
                                        font_size=15)
        self.up_move_button = Button(self.window, (self.loc[0] + 45, self.loc[1]), 30, 30, '↑', (200, 200, 200),
                                     (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.down_move_button = Button(self.window, (self.loc[0] + 45, self.loc[1] + 60), 30, 30, '↓', (200, 200, 200),
                                       (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.zoom_in_button = Button(self.window, (self.loc[0] + 75, self.loc[1]), 30, 30, '+', (200, 200, 200),
                                     (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.zoom_out_button = Button(self.window, (self.loc[0] + 15, self.loc[1]), 30, 30, '-', (200, 200, 200),
                                      (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.save = Button(self.window, (self.loc[0] + self.size[0] - 130, self.loc[1]), 40, 30, 'save',
                           (200, 200, 200), (0, 0, 0),
                           fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
    def AddItem(self, start_pos, end_pos, color=None, label: str = None, item_type=ARROW):
        """
        :param start_pos: you have to fill this anyway. If it is a POINT, this is the pos of the point.
        :param end_pos: if you are adding a POINT, leave this as None.
        :param color: RGB255mode.->(R, G, B)
        :param label: text,can be None.
        :param item_type: ONLY can be ARROW, POINT or LINE.
        :return: None
        """
        if item_type != POINT:
            self.coord_x_max = max(self.coord_x_max, max(start_pos[0], end_pos[0]))
            self.coord_x_min = min(self.coord_x_min, min(start_pos[0], end_pos[0]))
            self.coord_y_max = max(self.coord_y_max, max(start_pos[1], end_pos[1]))
            self.coord_y_min = min(self.coord_y_min, min(start_pos[1], end_pos[1]))
        else:
            self.coord_x_max = max(self.coord_x_max, start_pos[0])
            self.coord_x_min = min(self.coord_x_min, start_pos[0])
            self.coord_y_max = max(self.coord_y_max, start_pos[1])
            self.coord_y_min = min(self.coord_y_min, start_pos[1])
        if color is None:
            color = all_colours[self.num % len(all_colours)]
        if item_type == ARROW:
            self.arrows.append([start_pos, end_pos, color, label])
        elif item_type == POINT:
            self.points.append([start_pos, color, label])
        elif item_type == LINE:
            self.lines.append([start_pos, end_pos, color, label])
        else:
            return
        self.num += 1

    def RemoveItem(self, index, item_type=ARROW):
        if item_type == ARROW:
            del self.arrows[index]
        elif item_type == LINE:
            del self.lines[index]
        elif item_type == POINT:
            del self.points[index]

    def draw(self):
        plt.cla()
        plt.grid(True)
        plt.xlim(*self.last_lim[0:2])
        plt.ylim(*self.last_lim[2:4])
        plt.title(self.title)
        plt.xlabel(self.x_item_name)
        plt.ylabel(self.y_item_name)
        #colour is 255 mode. but the matplotlib uses 1.0 mode.
        for item in self.arrows:
            start_loc, end_loc, colour, text = item
            plt.quiver(*start_loc, *(end_loc[0] - start_loc[0], end_loc[1] - start_loc[1]),
                       color=colour, scale=1, scale_units='xy',
                       angles='xy')
            if text is not None:
                plt.text(*end_loc, color=colour, s=text)
        for item in self.lines:
            start_loc, end_loc, colour, text = item
            plt.plot(*start_loc, *end_loc, color=colour)
            if text is not None:
                plt.text(*end_loc, color=colour, s=text)
        for item in self.points:
            loc, colour, text = item
            plt.scatter(*loc, color=colour)
            if text is not None:
                plt.text(*loc, color=colour, s=text)
        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        screen = pygame.display.get_surface()
        size = canvas.get_width_height()
        surf = pygame.image.frombytes(raw_data, size, "RGB")
        screen.blit(surf, self.loc)
        if self.no_mouse:
            self.up_move_button.draw();self.down_move_button.draw()
            self.left_move_button.draw()
            self.reset_button.draw();self.right_move_button.draw()
            self.zoom_in_button.draw();self.zoom_out_button.draw()
        self.save.draw()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pass
        # 鼠标释放事件
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
            if self.no_mouse:
                if self.down_move_button.handle_event(event):
                    y_width = abs(self.last_lim[3] - self.last_lim[2])
                    dy = -0.04 * y_width
                    xlim = self.last_lim[0:2]
                    ylim = self.last_lim[2:4]
                    plt.ylim(ylim[0] + dy, ylim[1] + dy)
                    self.last_lim = [xlim[0], xlim[1], ylim[0] + dy, ylim[1] + dy]

                elif self.up_move_button.handle_event(event):
                    y_width = abs(self.last_lim[3] - self.last_lim[2])
                    dy = 0.04 * y_width
                    xlim = self.last_lim[0:2]
                    ylim = self.last_lim[2:4]
                    plt.ylim(ylim[0] + dy, ylim[1] + dy)
                    self.last_lim = [xlim[0], xlim[1], ylim[0] + dy, ylim[1] + dy]

                elif self.left_move_button.handle_event(event):
                    x_width = abs(self.last_lim[1] - self.last_lim[0])
                    dx = -0.04 * x_width
                    xlim = self.last_lim[0:2]
                    ylim = self.last_lim[2:4]
                    plt.xlim(xlim[0] + dx, xlim[1] + dx)
                    self.last_lim = [xlim[0] + dx, xlim[1] + dx, ylim[0], ylim[1]]

                elif self.right_move_button.handle_event(event):
                    x_width = abs(self.last_lim[1] - self.last_lim[0])
                    dx = 0.04 * x_width
                    xlim = self.last_lim[0:2]
                    ylim = self.last_lim[2:4]
                    plt.xlim(xlim[0] + dx, xlim[1] + dx)
                    self.last_lim = [xlim[0] + dx, xlim[1] + dx, ylim[0], ylim[1]]

                elif self.reset_button.handle_event(event):
                    self.last_lim = [self.coord_x_min, self.coord_x_max, self.coord_y_min, self.coord_y_max]

                elif self.zoom_out_button.handle_event(event):
                    self.last_lim = [1.1 * i for i in self.last_lim]

                elif self.zoom_in_button.handle_event(event):
                    self.last_lim = [0.9 * i for i in self.last_lim]
            if self.save.handle_event(event):
                type_selector = CheckBox(4,
                                         ['.png', '.svg', '.jpg', '.pdf'],
                                         4,
                                         self.window, self.clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30,
                                         buttons_adjust_length=0, background_color=(90, 90, 150))
                if len(type_selector.clicked_choices) == 0 or type(type_selector.clicked_choices) == str:
                    return

                current_time = datetime.datetime.now()
                file_name = str(current_time).split('.')[0].split(' ')[0] + '-' + \
                            str(current_time).split('.')[0].split(' ')[1]
                file_name = file_name.replace(':', '-')
                for i in type_selector.clicked_choices:
                    plt.savefig('Img/' + file_name + ['.png', '.svg', '.jpg', '.pdf'][i])

        # 鼠标按下事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_dragging = True
                self.last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 2:
                if not (self.loc[0] < event.pos[0] < self.loc[0] + self.size[0] and self.loc[1] < event.pos[1] <
                        self.loc[
                            1] + self.size[1]):
                    return
                self.last_lim = [self.coord_x_min, self.coord_x_max, self.coord_y_min, self.coord_y_max]

        # 鼠标移动事件
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                current_pos = pygame.mouse.get_pos()
                x_width = abs(self.last_lim[1] - self.last_lim[0])
                y_width = abs(self.last_lim[3] - self.last_lim[2])
                dx = (current_pos[0] - self.last_mouse_pos[0]) / 500 * x_width
                dy = (current_pos[1] - self.last_mouse_pos[1]) / 500 * y_width
                xlim = self.last_lim[0:2]
                ylim = self.last_lim[2:4]
                plt.xlim(xlim[0] - dx, xlim[1] - dx)
                plt.ylim(ylim[0] + dy, ylim[1] + dy)
                self.last_lim = [xlim[0] - dx, xlim[1] - dx, ylim[0] + dy, ylim[1] + dy]
                self.last_mouse_pos = current_pos

        # 添加滚轮缩放功能
        elif event.type == pygame.MOUSEWHEEL:
            # 获取当前缩放比例
            scale_factor = 1.1 if event.y < 0 else 0.9
            self.last_lim = [scale_factor * i for i in self.last_lim]


class CoordinateSystem3d:
    def __init__(self, window, loc, size, title='', no_mouse=False, axis_maxs=None, axes_mins=None, current_elev = 45,current_azim = -45):
        if axes_mins is None:
            axes_mins = [-5, -5, -5]
        if axis_maxs is None:
            axis_maxs = [5, 5, 5]
        plt.close('all')
        self.fig = plt.figure(figsize=(size[0] / 100, size[1] / 100),  # Inches
                              dpi=100)  # dots per inch
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.title = title
        self.size = size
        self.clock = pygame.time.Clock()
        self.no_mouse = no_mouse
        self.window, self.loc, self.size = window, loc, size
        self.points = []  # (loc, color, texts->None)
        self.lines = []  # (start-loc, end-loc, color, texts->None)
        self.arrows = []  # (start-loc, end-loc, color, texts->None)
        self.length = size[0]
        self.height = size[1]
        self.axes_maxes = axis_maxs
        self.axes_mins = axes_mins
        self.num = 0
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        self.current_elev = current_elev
        self.current_azim = current_azim
        self.fig.tight_layout()  # 自动调整布局
        plt.rcParams['axes.edgecolor'] = (0.5, 0.5, 0.5)  # 灰色坐标轴
        self.last_lim = [-5, 5, -5, 5, -5, 5]
        self.ax.view_init(elev=self.current_elev, azim=self.current_azim)

        self.left_move_button = Button(self.window, (self.loc[0], self.loc[1]+30), 30, 30, '<-', (200, 200, 200), (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.reset_button = Button(self.window, (self.loc[0]+30, self.loc[1]+30), 60, 30, 'reset', (200, 200, 200), (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.right_move_button = Button(self.window, (self.loc[0]+90, self.loc[1]+30), 30, 30, '->', (200, 200, 200), (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.up_move_button = Button(self.window, (self.loc[0]+45, self.loc[1]), 30, 30, '↑', (200, 200, 200),
                                        (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.down_move_button = Button(self.window, (self.loc[0] + 45, self.loc[1]+60), 30, 30, '↓', (200, 200, 200),
                                     (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.zoom_in_button = Button(self.window, (self.loc[0] + 75, self.loc[1]), 30, 30, '+', (200, 200, 200),
                                       (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.zoom_out_button = Button(self.window, (self.loc[0] + 15, self.loc[1]), 30, 30, '-', (200, 200, 200),
                                       (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)

        self.x_add_button = Button(self.window, (self.loc[0] + self.size[0] - 30, self.loc[1]), 30, 30, '+', (200, 200, 200),
                                      (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.x_minus_button = Button(self.window, (self.loc[0] + self.size[0] - 90, self.loc[1]), 30, 30, '-', (200, 200, 200),
                                      (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)

        self.y_add_button = Button(self.window, (self.loc[0] + self.size[0] - 30, self.loc[1] + 30), 30, 30, '+', (200, 200, 200),
                                      (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.y_minus_button = Button(self.window, (self.loc[0] + self.size[0] - 90, self.loc[1] + 30), 30, 30, '-', (200, 200, 200),
                                      (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)

        self.z_add_button = Button(self.window, (self.loc[0] + self.size[0] - 30, self.loc[1] + 60), 30, 30, '+', (200, 200, 200),
                                      (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.z_minus_button = Button(self.window, (self.loc[0] + self.size[0] - 90, self.loc[1] + 60), 30, 30, '-', (200, 200, 200),
                                      (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)

        self.z = Button(self.window, (self.loc[0] + self.size[0] - 60, self.loc[1] + 60), 30, 30, 'z',
                                     (200, 200, 200),
                                     (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.y = Button(self.window, (self.loc[0] + self.size[0] - 60, self.loc[1] + 30), 30, 30, 'y',
                                     (200, 200, 200),
                                     (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.x = Button(self.window, (self.loc[0] + self.size[0] - 60, self.loc[1]), 30, 30, 'x',
                                     (200, 200, 200),
                                     (0, 0, 0), fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.save = Button(self.window, (self.loc[0] + self.size[0] - 130, self.loc[1]), 40, 30, 'save', (200, 200, 200),(0, 0, 0),
                           fontName='fonts/JetBrainsMono-Light.ttf', font_size=15)
        self.mouse_wheel_direction = 1

    def AddItem(self, start_pos, end_pos, color=None, label: str = None, item_type=ARROW):
        """
        :param start_pos: you have to fill this anyway. If it is a POINT, this is the pos of the point.
        :param end_pos: if you are adding a POINT, leave this as None.
        :param color: RGB255mode.->(R, G, B)
        :param label: text,can be None.
        :param item_type: ONLY can be ARROW, POINT or LINE.
        :return: None
        """
        sx, sy, sz = start_pos
        if item_type != POINT:
            ex, ey, ez = end_pos
        else:
            ex = ey = ez = 0
        max_x, max_y, max_z = self.axes_maxes
        min_x, min_y, min_z = self.axes_mins
        self.axes_maxes = [max(sx, ex, max_x), max(sy, ey, max_y), max(sz, ez, max_z)]
        self.axes_mins = [min(sx, ex, min_x), min(sy, ey, min_y), min(sz, ez, min_z)]
        if color is None:
            color = all_colours[self.num % len(all_colours)]
        if item_type == ARROW:
            self.arrows.append([start_pos, end_pos, color, label])
        elif item_type == POINT:
            self.points.append([start_pos, color, label])
        elif item_type == LINE:
            self.lines.append([start_pos, end_pos, color, label])
        else:
            return
        self.num += 1
        self.last_lim = [self.axes_mins[0], self.axes_maxes[0],
                         self.axes_mins[1], self.axes_maxes[1],
                         self.axes_mins[2], self.axes_maxes[2]]

    def RemoveItem(self, index, item_type=ARROW):
        if item_type == ARROW:
            del self.arrows[index]
        elif item_type == LINE:
            del self.lines[index]
        elif item_type == POINT:
            del self.points[index]

    def draw(self):
        self.ax.clear()
        plt.cla()
        self.ax.set_xlim3d(self.last_lim[0:2])
        self.ax.set_ylim3d(self.last_lim[2:4])
        self.ax.set_zlim3d(self.last_lim[4:6])
        self.ax.grid(True)
        self.ax.set_title(self.title)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.scatter(0, 0, 0)
        #colour is 255 mode. but the matplotlib uses 1.0 mode.
        for item in self.arrows:
            start_loc, end_loc, colour, text = item
            self.ax.quiver(*start_loc, *(end_loc[0] - start_loc[0], end_loc[1] - start_loc[1], end_loc[2] - start_loc[2]),
                       color=colour)
            if self.num >= 3:
                self.draw_3d_mark_lines(end_loc, self.ax, color=colour)
                if start_loc != (0, 0, 0):
                    self.draw_3d_mark_lines(start_loc, self.ax, color=colour)
            else:
                plot_dashed_cuboid(*(end_loc[0] - start_loc[0], end_loc[1] - start_loc[1], end_loc[2] - start_loc[2]),
                                   self.ax, start_loc, color=colour)
            if text is not None:
                self.ax.text(*end_loc, text, color=colour)
        for item in self.lines:
            start_loc, end_loc, colour, text = item
            self.ax.plot(*start_loc, *end_loc, color=colour)
            if self.num >= 3:
                self.draw_3d_mark_lines(end_loc, self.ax, color=colour)
                if start_loc != (0, 0, 0):
                    self.draw_3d_mark_lines(start_loc, self.ax, color=colour)
            else:
                plot_dashed_cuboid(*(end_loc[0] - start_loc[0], end_loc[1] - start_loc[1], end_loc[2] - start_loc[2]),
                                   self.ax, start_loc, color=colour)
            if text is not None:
                self.ax.text(*end_loc, text, color=colour)
        for item in self.points:
            loc, colour, text = item
            self.ax.scatter(*loc, color=colour)
            if self.num >= 3:
                self.draw_3d_mark_lines(loc, self.ax, color=colour)
            else:
                plot_dashed_cuboid(*loc, self.ax)
            if text is not None:
                self.ax.text(*loc, color=colour, s=text)

        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.canvas.draw()
        self.renderer = self.canvas.get_renderer()
        self.raw_data = self.renderer.buffer_rgba()


        size = self.canvas.get_width_height()
        surf = pygame.image.frombuffer(self.raw_data, size, "RGBA")
        self.window.blit(surf, self.loc)
        surf.set_alpha(255)
        updated_rect = surf.get_rect()
        self.window.blit(surf, self.loc, updated_rect)
        if self.no_mouse:
            self.up_move_button.draw();self.down_move_button.draw()
            self.left_move_button.draw()
            self.reset_button.draw();self.right_move_button.draw()
            self.zoom_in_button.draw();self.zoom_out_button.draw()
        self.x_add_button.draw();self.x_minus_button.draw()
        self.y_add_button.draw();self.y_minus_button.draw()
        self.z_add_button.draw();self.z_minus_button.draw()
        self.x.draw();self.y.draw();self.z.draw()
        self.save.draw()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return None
        elif event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.loc[0] + self.size[0] > mouse_x > self.loc[0] + self.size[0] - 90 and self.loc[1] < mouse_y < self.loc[1] + 90:
                self.mouse_wheel_direction = 1 if event.y < 0 else -1
                return False
            scale_factor = 1.1 if event.y < 0 else 0.9
            self.last_lim = [scale_factor * i for i in self.last_lim]
            return None
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.no_mouse:
                if self.down_move_button.handle_event(event):
                    self.current_elev -= 10
                    self.current_elev = np.clip(self.current_elev, 1, 89)
                    # 更新3D视图
                    self.ax.view_init(elev=self.current_elev, azim=self.current_azim)

                    # 重新渲染图表
                    self.canvas.draw()
                    self.raw_data = self.renderer.buffer_rgba()

                elif self.up_move_button.handle_event(event):
                    self.current_elev += 10
                    self.current_elev = np.clip(self.current_elev, 1, 89)
                    # 更新3D视图
                    self.ax.view_init(elev=self.current_elev, azim=self.current_azim)

                    # 重新渲染图表
                    self.canvas.draw()
                    self.raw_data = self.renderer.buffer_rgba()

                elif self.left_move_button.handle_event(event):
                    self.current_azim -= 10
                    self.current_azim %= 360
                    # 更新3D视图
                    self.ax.view_init(elev=self.current_elev, azim=self.current_azim)

                    # 重新渲染图表
                    self.canvas.draw()
                    self.raw_data = self.renderer.buffer_rgba()

                elif self.right_move_button.handle_event(event):
                    self.current_azim += 10
                    self.current_azim %= 360
                    # 更新3D视图
                    self.ax.view_init(elev=self.current_elev, azim=self.current_azim)

                    # 重新渲染图表
                    self.canvas.draw()
                    self.raw_data = self.renderer.buffer_rgba()

                elif self.reset_button.handle_event(event):
                    self.current_elev = 45
                    self.current_azim = -45
                    self.ax.view_init(elev=self.current_elev, azim=self.current_azim)
                    self.last_lim = [self.axes_mins[0], self.axes_maxes[0],
                                     self.axes_mins[1], self.axes_maxes[1],
                                     self.axes_mins[2], self.axes_maxes[2]]
                    self.canvas.draw()

                elif self.zoom_out_button.handle_event(event):
                    self.last_lim = [1.1 * i for i in self.last_lim]

                elif self.zoom_in_button.handle_event(event):
                    self.last_lim = [0.9 * i for i in self.last_lim]
            if self.x_add_button.handle_event(event):
                x_abs = abs(self.last_lim[1]-self.last_lim[0])
                self.last_lim = [self.last_lim[0] + 0.1*x_abs*self.mouse_wheel_direction, self.last_lim[1] + 0.1*x_abs*self.mouse_wheel_direction, *self.last_lim[2:6]]
            elif self.x_minus_button.handle_event(event):
                x_abs = abs(self.last_lim[1] - self.last_lim[0])
                self.last_lim = [self.last_lim[0] - 0.1 * x_abs*self.mouse_wheel_direction, self.last_lim[1] - 0.1 * x_abs*self.mouse_wheel_direction, *self.last_lim[2:6]]
            elif self.y_add_button.handle_event(event):
                y_abs = abs(self.last_lim[3]-self.last_lim[2])
                self.last_lim = [*self.last_lim[0:2], self.last_lim[2] + 0.1*y_abs*self.mouse_wheel_direction, self.last_lim[3] + 0.1*y_abs*self.mouse_wheel_direction, *self.last_lim[4:6]]
            elif self.y_minus_button.handle_event(event):
                y_abs = abs(self.last_lim[3] - self.last_lim[2])
                self.last_lim = [*self.last_lim[0:2], self.last_lim[2] - 0.1 * y_abs*self.mouse_wheel_direction, self.last_lim[3] - 0.1 * y_abs*self.mouse_wheel_direction,
                                     *self.last_lim[4:6]]
            elif self.z_add_button.handle_event(event):
                z_abs = abs(self.last_lim[5] - self.last_lim[4])
                self.last_lim = [*self.last_lim[0:4], self.last_lim[4] + 0.1 * z_abs*self.mouse_wheel_direction, self.last_lim[5] + 0.1 * z_abs*self.mouse_wheel_direction]
            elif self.z_minus_button.handle_event(event):
                z_abs = abs(self.last_lim[5] - self.last_lim[4])
                self.last_lim = [*self.last_lim[0:4], self.last_lim[4] - 0.1 * z_abs*self.mouse_wheel_direction, self.last_lim[5] - 0.1 * z_abs*self.mouse_wheel_direction]
            elif self.save.handle_event(event):
                type_selector = CheckBox(4,
                                         ['.png', '.svg', '.jpg', '.pdf'],
                                         4,
                                         self.window, self.clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30,
                                         buttons_adjust_length=0, background_color=(90, 90, 150))
                if len(type_selector.clicked_choices) == 0 or type(type_selector.clicked_choices) == str:
                    return None

                current_time = datetime.datetime.now()
                file_name = str(current_time).split('.')[0].split(' ')[0]+'-'+str(current_time).split('.')[0].split(' ')[1]
                file_name = file_name.replace(':', '-')
                for i in type_selector.clicked_choices:
                    plt.savefig('Img/'+file_name+['.png', '.svg', '.jpg', '.pdf'][i])

            if event.button == 1:  # 左键释放
                self.dragging = False
                return None
            return None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > self.loc[0] + self.size[0] - 90 and mouse_y < 90:
                return False
            if event.button == 1:  # 右键按下
                self.dragging = True
                self.last_mouse_pos = event.pos
                pygame.mouse.get_rel()  # 重置相对移动量
                return None
            elif event.button == 2:
                if not (self.loc[0] < event.pos[0] < self.loc[0] + self.size[0] and self.loc[1] < event.pos[1] <
                        self.loc[
                            1] + self.size[1]):
                    return None
                # 添加视角复位功能
                self.current_elev = 45
                self.current_azim = -45
                self.ax.view_init(elev=self.current_elev, azim=self.current_azim)
                self.last_lim = [self.axes_mins[0], self.axes_maxes[0],
                                 self.axes_mins[1], self.axes_maxes[1],
                                 self.axes_mins[2], self.axes_maxes[2]]
                self.canvas.draw()
                return None
            return None

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            if not (self.loc[0] < event.pos[0] < self.loc[0] + self.size[0] and self.loc[1] < event.pos[1] < self.loc[1] + self.size[1]):
                return None
            # 获取相对移动量
            dx, dy = pygame.mouse.get_rel()

            # 更新视角参数
            self.current_azim += -dx * sensitivity
            self.current_elev -= -dy * sensitivity  # 注意方向

            # 限制角度范围
            self.current_elev = np.clip(self.current_elev, 1, 89)  # 防止上下翻转
            self.current_azim %= 360  # 保持方位角在0-360范围内

            # 更新3D视图
            self.ax.view_init(elev=self.current_elev, azim=self.current_azim)

            # 重新渲染图表
            self.canvas.draw()
            self.raw_data = self.renderer.buffer_rgba()
            return None
        return None

    def draw_3d_mark_lines(self, loc, ax, color:str):
        self.ax.plot([loc[0], loc[0]], [self.last_lim[2], loc[1]], [loc[2], loc[2]], linestyle='--', color=color)
        self.ax.plot([self.last_lim[0], loc[0]], [loc[1], loc[1]], [loc[2], loc[2]], linestyle='--', color=color)
        self.ax.plot([loc[0], loc[0]], [loc[1], loc[1]], [self.last_lim[4], loc[2]], linestyle='--', color=color)


class Button:
    def __init__(self,window,loc, width, height, text, bg_color, text_color, font_size=30, fontName=None):
        self.rect = pygame.Rect(*loc, width, height)
        self.window = window
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.fontName = fontName
        self.font = pygame.font.Font(self.fontName, font_size)

    def draw(self):
        pygame.draw.rect(self.window, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.window.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos
            return self.rect.collidepoint(mouse_pos)

    def setValue(self, string):
        self.text = string


def pygame_draw_arrow(window, start_pos, end_pos, width=10, color=(0, 192, 255)):
    dx, dy = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
    if math.sqrt((dx * 0.2) ** 2 + (dy * 0.2) ** 2) * 1.73 >= width:
        line_end = start_pos[0] + dx * 0.8, start_pos[1] + dy * 0.8
    else:
        y = math.sqrt((width + 4) / ((dx / dy) + 1))
        x = dx / dy * y
        line_end = start_pos[0] + x, start_pos[1] + y
    pygame.draw.circle(window, color, (start_pos[0], start_pos[1] + 1), width // 2)
    pygame.draw.line(window, color, start_pos, line_end, width)
    triangle_end_point = end_pos
    triangle_bottom_mid = line_end
    x1, y1 = triangle_end_point
    x2, y2 = triangle_bottom_mid
    sq3 = math.sqrt(3)
    triangle_other_point1 = (x2 + (y2 - y1) / sq3, y2 - (x2 - x1) / sq3)
    triangle_other_point2 = (x2 - (y2 - y1) / sq3, y2 + (x2 - x1) / sq3)
    pygame.draw.polygon(window, color, [triangle_other_point1, triangle_other_point2, triangle_end_point])


def plot_dashed_cuboid(length, width, height, ax, lower_left=(0, 0, 0), color=''):
    """
    :param length: length : float    - x length
    :param width: width  : float    - y length
    :param height: height : float    - z length
    :param lower_left: lower_left : tuple - cor(the left bottom point) (x0, y0, z0)
    :param ax:
    :param fig:
    :return:
    """
    ax = ax

    x0, y0, z0 = lower_left

    # generate 8 points' cors
    vertices = np.array([
        # bottom rect
        [x0, y0, z0],
        [x0 + length, y0, z0],
        [x0 + length, y0 + width, z0],
        [x0, y0 + width, z0],
        # top rect
        [x0, y0, z0 + height],
        [x0 + length, y0, z0 + height],
        [x0 + length, y0 + width, z0 + height],
        [x0, y0 + width, z0 + height],
    ])

    # define connection relationships.
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # bottom
        (4, 5), (5, 6), (6, 7), (7, 4),  # top
        (0, 4), (1, 5), (2, 6), (3, 7)  # side
    ]

    # draw sides
    for edge in edges:
        start, end = vertices[edge[0]], vertices[edge[1]]
        ax.plot(*zip(start, end),
                linestyle='--',
                color=color,
                linewidth=0.5,
                alpha=0.7)





if __name__ == '__main__':
    # 设置窗口大小
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF)
    #b = CoordinateSystem2d(screen, (0, 0), (800, 600))
    a = CoordinateSystem3d(screen, (0, 0), (800, 600), no_mouse=False)
    #a.AddItem((0, 0, 0), (4, 1, 3),label='a')
    a.AddItem((1, 1, 1), (4, 4, 3), label='b')
    a.AddItem((2, 2, 2), (4, 1, 3),label='c')
    # 游戏主循环
    running = True
    while running:
        events = pygame.event.get()
        wheel_events, other = [], []
        for curr in events:
            if curr.type == pygame.MOUSEWHEEL:
                wheel_events.append(curr)
            else:
                other.append(curr)
        events = wheel_events + other
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            a.handle_event(event)
            #b.handle_event(event)
        # 填充背景色为白色
        screen.fill((255, 255, 255))
        a.draw()
        #b.draw()
        pygame.display.flip()

    # 退出pygame
    pygame.quit()
