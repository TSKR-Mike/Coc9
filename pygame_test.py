import pygame
import sys
from checkbox import CheckBox
import pyghelpers
pygame.init()
from statistics import Message_window
m = Message_window()
window = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
charting_type_selector = CheckBox(8, ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface(Not recommended)',
                                              'bar plots', 'quivers', 'contour'], 8,
                                          window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30,
                                          buttons_adjust_length=0, background_color=(90, 90, 150))
pygame.quit()
sys.exit()
