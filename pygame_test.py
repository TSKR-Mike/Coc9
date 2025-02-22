import pygame
import sys
from checkbox import CheckBox
import pyghelpers
pygame.init()
from statistics import Message_window
m = Message_window()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
charts_type = CheckBox(8, ['hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'], 8,
                     screen, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30,buttons_adjust_length=0,
                     background_color=(90, 90, 150))
num = pyghelpers.textAnswerDialog(screen, (0, 0, 1004, 200), 'How many ' +
                                                  ['hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin',
                                                   'plot', 'scatter'][0] + ' charts do you want to draw?',
                                                  'OK',
                                                  'CANCEL', backgroundColor=(90, 90, 150),
                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
pygame.quit()
sys.exit()
