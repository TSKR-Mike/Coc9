import time, sys, threading, platform
import pygame
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN, SCRAP_TEXT
from Scroller import VerticalScroller, HorizontalScroller
import threading

import threading
import pygame
from pygame.locals import MOUSEBUTTONDOWN


IS_ALPHA = 0
IS_DIGIT = 1
IS_SYMBOL = 2
IS_CHINESE = 3
def identify_char(char):
    if '\u4e00' <= char <= '\u9fff':
        return IS_CHINESE
    elif char.isalpha():
        return IS_ALPHA
    elif char.isdigit():
        return IS_DIGIT
    else:
        return IS_SYMBOL

def get_char_width(char):
    type_ = identify_char(char)
    if type_ in [IS_ALPHA, IS_SYMBOL, IS_DIGIT]:
        return 10
    elif type_ == IS_CHINESE:
        return 20


class ControlId(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.id = 1
        self.click_id = -1

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(ControlId, "_instance"):
            ControlId._instance = ControlId(*args, **kwargs)
        return ControlId._instance

    def get_new_id(self):
        self.id += 1
        return self.id


class Base(object):
    def __init__(self):
        self.panel = None
        self._visible = True
        self._text_align = TEXT_ALIGN_MIDDLE
        self._font = DEFAULT_SM_FONT
        self.ctl_id = ControlId().instance().get_new_id()

    def init_font(self):
        pass

    def clear_foucs(self):
        pass

    def clear_hover(self):
        pass

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    @property
    def text_align(self):
        return self._text_align

    @text_align.setter
    def text_align(self, value):
        self._text_align = value
        self.init_font()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self.init_font()


CLICK_EFFECT_TIME = 100
DEFAULT_FONT = pygame.font.Font("simhei.ttf", 28)
DEFAULT_SM_FONT = pygame.font.Font("simhei.ttf", 20)


def get_default_font(size):
    return pygame.font.Font("simhei.ttf", int(size))


TEXT_ALIGN_LEFT = 1
TEXT_ALIGN_MIDDLE = 2
TEXT_ALIGN_RIGHT = 3


black = (50, 50, 50)
pygame.init()

class ColInfo(object):
    def __init__(self, surface, name, font_image=None, x=0, y=0,LeftTop=(0, 0)):
        self.surface = surface
        self.x = x
        self.y = y
        self.name = name
        self.font_image = font_image
        self.LeftTop = LeftTop

    def draw(self):
        if self.surface: self.surface.blit(self.font_image, (self.x + self.LeftTop[0], self.y + self.LeftTop[1]))


class RowItem(object):
    def __init__(self, surface, val, font_image=None, x=0, y=0, LeftTop=(0, 0)):
        self.surface = surface
        self.x = x
        self.y = y
        self.val = val
        self.font_image = font_image
        self.LeftTop = LeftTop

    def draw(self):
        if self.surface: self.surface.blit(self.font_image, (self.x + self.LeftTop[0], self.y + self.LeftTop[1]))


class RowInfo(object):
    def __init__(self):
        self.row_items = []
        self.highlight = False
        self.surface = None
        self.rect = None

    def draw(self):
        if self.highlight and self.surface:
            pygame.draw.rect(self.surface, (218, 245, 255), self.rect)
        else:
            pygame.draw.rect(self.surface, (255, 255, 255), self.rect)
        for row_item in self.row_items:
            row_item.draw()


class Table(Base):
    def __init__(self, parent, loc, columns, rows, grid_colour = (100, 100, 100)):
        super(Table, self).__init__()
        self.x, self.y = loc
        self.bg_color, self.grid_colour = (255, 255, 255), grid_colour
        self.parent = parent
        self._row_height = 30
        self.row_num = len(rows) + 1
        self.height = self.row_num * self._row_height
        self.in_click = False
        self.click_loss_time = 0
        self.click_event_id = -1
        self.ctl_id = ControlId().instance().get_new_id()
        self.header_list = []
        self._header_height = 30
        self.widths = [0 for i in range(len(rows[0])+1)]
        for line in rows:
            for item, index in zip(line, range(len(line))):
                current_item_width = 0
                for char in str(item):
                    current_item_width += get_char_width(char)
                if current_item_width >= self.widths[index]:
                    self.widths[index] = current_item_width

        for item, index in zip(columns, range(len(columns))):
            current_item_width = 0
            for char in str(item):
                current_item_width += get_char_width(char)
            if current_item_width >= self.widths[index]:
                self.widths[index] = current_item_width
        self.width = sum(self.widths)
        self.surface = parent
        self.rows_content = rows
        self.column_content = columns
        self._col_font = get_default_font(self._header_height * 0.5)
        self._row_font = get_default_font(self._row_height * 0.6)

        self._columns = []
        # creating columns obj.(headers)
        for i in range(len(columns)):
            col = columns[i]
            col_info = ColInfo(self.surface,
                               col, LeftTop=(sum(self.widths[0:i]) + self.x, 0 + self.y))
            header_image = self._col_font.render(str(col), True, black)
            w, h = header_image.get_size()
            col_info.x = (self.widths[i] - w) / 2
            col_info.y = (self._header_height - h) / 2
            col_info.font_image = header_image
            self._columns.append(col_info)
        # creating row obj.(actual data)
        self._rows = []
        for i in range(len(rows)):
            y = self._header_height + self._row_height * i
            row = rows[i]
            row_info = RowInfo()
            row_info.rect = (self.x, y + self.y, self.width, self._row_height)
            row_info.surface = self.parent
            if i % 2 == 1: row_info.highlight = True
            for j in range(len(row)):
                v = row[j]
                item = RowItem(self.parent, v, LeftTop=(sum(self.widths[0:j]) + self.x, y + self.y))
                v = str(v)
                row_image = self._row_font.render(v, True, black)
                w, h = row_image.get_size()
                item.x = (self.widths[j] - w) / 2
                item.y = (self._row_height - h) / 2
                item.font_image = row_image
                row_info.row_items.append(item)
            self._rows.append(row_info)

    def clear_foucs(self):
        self.in_edit = False

    def update(self, event):
        return False

    def draw(self):
        if not self._visible:
            return

        pygame.draw.rect(self.parent, (200, 200, 200), (self.x, self.y, self.width, self._header_height))
        pygame.draw.rect(self.surface, self.grid_colour,
                         (self.x, self.y, self.width, self._header_height + self._row_height * len(self._rows)), 1)
        pygame.draw.line(self.surface, self.grid_colour, [self.x, self._header_height + self.y], [self.width + self.x, self._header_height + self.y], 1)
        for col_info in self._columns:
            col_info.draw()
        for row_info in self._rows:
            row_info.draw()
        for i in range(1, len(self._rows)):
            y = self._header_height + i * self._row_height
            pygame.draw.line(self.surface, self.grid_colour, [self.x, y + self.y], [self.width + self.x, y + self.y], 1)
        for i in range(1, len(self._columns)):
            x = sum(self.widths[0:i])
            pygame.draw.line(self.surface, self.grid_colour, [x + self.x, self.y],
                             [x + self.x, self._header_height + self._row_height * len(self._rows) + self.y], 1)

        #draw the frame
        pygame.draw.rect(self.surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)

    def relocate(self):
        col_num = len(self.column_content)
        self._columns = []
        for i in range(col_num):
            col = self.column_content[i]
            col_info = ColInfo(self.surface,
                               col, LeftTop=(sum(self.widths[0:i]) + self.x, 0 + self.y))
            header_image = self._col_font.render(str(col), True, black)
            w, h = header_image.get_size()
            col_info.x = (self.widths[i] - w) / 2
            col_info.y = (self._header_height - h) / 2
            col_info.font_image = header_image
            self._columns.append(col_info)
        self._rows = []
        for i in range(len(self.rows_content)):
            y = self._header_height + self._row_height * i
            row = self.rows_content[i]
            row_info = RowInfo()
            row_info.rect = (self.x, y + self.y, self.width, self._row_height)
            row_info.surface = self.parent
            if i % 2 == 1: row_info.highlight = True
            for j in range(len(row)):
                v = row[j]
                item = RowItem(self.parent, v, LeftTop=(sum(self.widths[0:j]) + self.x, y + self.y))
                v = str(v)
                row_image = self._row_font.render(v, True, black)
                w, h = row_image.get_size()
                item.x = (self.widths[j] - w) / 2
                item.y = (self._row_height - h) / 2
                item.font_image = row_image
                row_info.row_items.append(item)
            self._rows.append(row_info)


class WindowListViewer:

    def __init__(self, data:list[list]|list[tuple]|tuple[tuple]|tuple[list], maxsize:tuple[int,int], window=None, loc:tuple[int, int]=(0, 0), auto_heading=True):
        super().__init__()
        self.running = True
        pygame.init()
        if auto_heading:
            data_modified = [['#']]
            for i in range(len(data)):
                data_modified.append([i])
            for i in range(len(data[0])):data_modified[0].append(str(i))
            for index in range(len(data)):
                data_modified[index+1].extend(data[index])
        else:
            data_modified = data

        widths = [0 for i in range(len(data_modified[0])+1)]
        for line in data_modified:
            for item, index in zip(line, range(len(line))):
                current_item_width = 0
                for char in str(item):
                    current_item_width += get_char_width(char)
                if current_item_width >= widths[index]:
                    widths[index] = current_item_width

        self.width = sum(widths)
        self.height = len(data_modified) * 30
        self.headers = data_modified[0]
        self.data = data_modified[1:len(data_modified)]
        self.locCache = 0, 0
        self.loc = loc
        # locCache is used to tell if the scrollbars were moved; if they weren't,
        # there's no needs to relocate the table which slows down the program.
        self.table_loc_x, self.table_loc_y = 0, 0
        self.SmallerX, self.SmallerY = False ,False
        self.widthRatio, self.heightRatio = 1.0, 1.0
        if self.width-20 >= maxsize[0]:
            self.widthRatio = self.width / (maxsize[0]-20)
            self.width = maxsize[0]
            self.SmallerX = True
            # Table-width:Window-width = Total-width(of the scroller):Bar-width; <-----------------------------\
            # So W-w*Tot-w = B-w*Tab-w ==> B-w = (W-w)*(Tot-w)/(Tab-w), and THE RATIO is ----------------------/ (the one above)
            # Therefore, the distance that the table window has to move equals to scroller_x*ratio [NOTING THAT W-w NOT ALWAYS EQUALS TO Tot-w]
        if self.height >= maxsize[1]-20:
            self.heightRatio = self.height / maxsize[1]
            self.height = maxsize[1]
            self.SmallerY = True
            # the same as the x
        self.window = pygame.display.set_mode((self.width, self.height)) if window is None else window
        if self.SmallerX:
            self.ScrollerX = HorizontalScroller(self.window, loc[0], self.height - 20 + loc[1], 20, self.width * (self.width - 20) / (self.width * self.widthRatio), self.width - 20)
        if self.SmallerY:
            self.ScrollerY = VerticalScroller(self.window, self.width-20+loc[0], loc[1], self.height*(self.height-20)/(self.height*self.heightRatio), 20, self.height)
        self.table = Table(self.window, (self.table_loc_x + loc[0], self.table_loc_y + loc[1]), self.headers, self.data)

    def draw(self, update=False):
        self.table.draw()
        if self.SmallerX:
            self.ScrollerX.draw()
        if self.SmallerY:
            self.ScrollerY.draw()
        if update:
            pygame.display.update()

    def handle_event(self, event):
        locUpdated = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if self.SmallerX:
            self.ScrollerX.handle_event(event)
            if self.ScrollerX.scroller_x != self.locCache[0]:
                self.table_loc_x = -self.ScrollerX.scroller_x * self.widthRatio
                locUpdated = True
        if self.SmallerY:
            self.ScrollerY.handle_event(event)
            if self.ScrollerY.scroller_y != self.locCache[1]:
                self.table_loc_y = -self.ScrollerY.scroller_y * self.heightRatio
                locUpdated = True
        if locUpdated:
            self.locCache = self.table_loc_x, self.table_loc_y
            self.table.x, self.table.y = self.table_loc_x + self.loc[0], self.table_loc_y + self.loc[1]
            self.table.relocate()


if __name__ == '__main__':
    pass