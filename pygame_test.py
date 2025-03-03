import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
fig = plt.figure()  # 创建一个Figure对象
ax = fig.add_subplot(111)  # 添加一个子图
ax.plot([1, 2, 3], [4, 5, 6])  # 在子图上绘制图形
ax.set_title('示例图形')

# 保存图形
fig.savefig('Img/example_plot_with_figure.png')  # 使用Figure对象的savefig方法
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
