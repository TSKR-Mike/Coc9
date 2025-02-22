

import sys
import threading
import time

import pygame

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((700, 620))

from Panel import Panel
from Table import Table

pygame.display.set_caption('bf control')

btn_panel = Panel()
#alphas, symbols and digits: 10 per char
#chinese:20 per char
headers = (0, 1, 2, 3, 4)
rows = []
rows.append((u'a', 11, 99, 95, 91))
rows.append((u'你好吗不会要', 10, 9755, 88, 78))
rows.append((u'003', 11, 99, 100, 100))
rows.append((u'809', 11, 99, 95, 91))
rows.append((u'345', 10, 97, 88, 90))
rows.append((u'654', 11, 99, 100, 100))
rows.append((u'765', 11, 99, 95, 91))
rows.append((u'334', 10, 97, 88, 90))
rows.append((u'2354', 11, 99, 100, 100))
rows.append((u'436', 11, 99, 95, 91))
rows.append((u'777', 10, 97, 88, 90))
rows.append((u'844', 11, 99, 100, 100))
table = Table(screen, (20, 20), headers, rows)
btn_panel.add_control(table)
from Table import WindowListViewer
a = WindowListViewer(rows, (300,300), window=screen, loc=(0,0))
while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen = 0
            exit()
        #btn_panel.update(event)
        a.handle_event(event)
    a.draw()
    table.x -= 0.1
    table.relocate()
    #btn_panel.draw()
    pygame.display.update()
