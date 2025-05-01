import time

import pygame
import pygwidgets
from pygame.locals import *

from progress_bar import DotCircledProgressBar
from statistics import Message_window
message_window = Message_window()

try:
    from rich.traceback import install
    install(show_locals=True)
except:pass


def is_float(s):
    pattern = re.compile(r'^-?\d*\.?\d+$')
    return bool(pattern.match(s))


def draw_all():
    """
    draw all the buttons, text fields and else things.
    """
    global line1, line2, line3, line4_1, line4_2, line4_2, line5, line6, line7, warning_text, science
    global answertext, mode_text, backspace, text
    text.draw()
    answertext.draw()
    mode_text.draw()
    line1.drawAllButtons()
    line2.drawAllButtons()
    line3.drawAllButtons()
    line4_1.drawAllButtons()
    line4_2.drawAllButtons()
    line5.drawAllButtons()
    line6.drawAllButtons()
    line7.drawAllButtons()
    science.draw()
    backspace.draw()
    warning_text.draw()


def get_number_key(event):
    # 获取修饰键状态（Shift, Ctrl, Alt 等）
    modifiers = pygame.key.get_mods()

    # 判断是否按下了 Shift
    shift_pressed = modifiers & pygame.KMOD_SHIFT
    if shift_pressed: return None
    if event.key == pygame.K_0:
        return 0
    elif event.key == pygame.K_1:
        return 1
    elif event.key == pygame.K_2:
        return 2
    elif event.key == pygame.K_3:
        return 3
    elif event.key == pygame.K_4:
        return 4
    elif event.key == pygame.K_5:
        return 5
    elif event.key == pygame.K_6:
        return 6
    elif event.key == pygame.K_7:
        return 7
    elif event.key == pygame.K_8:
        return 8
    elif event.key == pygame.K_9:
        return 9
    return None


def get_calcu_symbol_key(event):
    # 获取修饰键状态（Shift, Ctrl, Alt 等）
    modifiers = pygame.key.get_mods()

    # 判断是否按下了 Shift
    shift_pressed = modifiers & pygame.KMOD_SHIFT
    if event.key == pygame.K_EQUALS and shift_pressed:
        return '+'
    elif event.key == pygame.K_8 and shift_pressed:
        return '*'
    elif event.key == pygame.K_9 and shift_pressed:
        return '('
    elif event.key == pygame.K_0 and shift_pressed:
        return ')'
    elif event.key == pygame.K_MINUS:
        return '-'
    elif event.key == pygame.K_1 and shift_pressed:
        return '!'
    elif event.key == pygame.K_6 and shift_pressed:
        return '^'
    else:
        key_name = pygame.key.name(event.key)
        if key_name == '/':
            return '/'
        elif key_name == '.':
            return '.'
        return None


import re

pattern = re.compile(r'(\d+)(√)')
reverse_pattern = re.compile(r'([⁰¹²³⁴⁵⁶⁷⁸⁹]+)(?!√)')


def convert_sqrt_expression(s):
    global pattern, reverse_pattern
    superscript_map = {
        '0': '⁰',
        '1': '¹',
        '2': '²',
        '3': '³',
        '4': '⁴',
        '5': '⁵',
        '6': '⁶',
        '7': '⁷',
        '8': '⁸',
        '9': '⁹'
    }
    reverse_superscript_map = {v: k for k, v in superscript_map.items()}

    def replacer(match):
        number = match.group(1)
        sqrt_symbol = match.group(2)
        superscript = ''.join([superscript_map[d] for d in number])
        return superscript + sqrt_symbol

    converted = pattern.sub(replacer, s)

    def reverse_replacer(match):
        sup_chars = match.group(1)
        normal = ''.join([reverse_superscript_map.get(c, c) for c in sup_chars])
        return normal

    final = reverse_pattern.sub(reverse_replacer, converted)

    return final


pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((1004, 610), DOUBLEBUF)
window.fill((0, 191, 255))
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption('Collections of Calculation')
pygame.display.update()
loading_obj = DotCircledProgressBar(window, clock, (502, 300), 100, 10, (0, 191, 255))
loading_obj.run()
loading = pygwidgets.DisplayText(window, (80, 450), 'Loading dependencies...7% complete',
                                 textColor=(255, 255, 255), backgroundColor=(0, 191, 255), fontSize=40,
                                 fontName='fonts/JetBrainsMono-Light.ttf')
loading.draw()
try:
    import math
    import sys
    import pyghelpers

    loading.setValue('Loading dependencies...15% complete')
    loading.draw()
    import numpy as np
    import scipy

    loading.setValue('Loading dependencies...31% complete')
    loading.draw()

    import sympy

    from sympy import Integral

    loading.setValue('Loading dependencies...57% complete')
    loading.draw()

    from buttoncenter import *
    import matplotlib.pyplot as plt
    import matplotlib

    matplotlib.use('WXagg')
    ax = plt.gca()
    loading.setValue('Loading dependencies...81% complete')
    loading.draw()

    from EventPyghelpers import textNumberDialogEventProgressing
    from complex import ComplexUi
    from matrix import MatrixUi
    from vector import VectorUi

    loading.setValue('Loading dependencies...94% complete')
    loading.draw()
    ########################################################
    from statistics import data_visualize_2d, data_analyze, data_comparison, data_distribution, \
        data_visualize_3d
    ######################################################
    from checkbox import CheckBox
    from progress_bar import windows_progress_bar
    import pyperclip
    from MathsCalculation import Calculation
    from UsrGuide import UsrNotice

except ModuleNotFoundError as e:
    loading_obj.done()
    try:
        font = pygame.font.Font('fonts/JetBrainsMono-Light.ttf')
    except:
        font = pygame.font.Font()
    text = font.render('Failed to launch Coc because of a dependence can not be loaded:' + str(e).split("'")[1], True,
                       (255, 0, 0))
    text2 = font.render('Press any key to quit.', True,
                        (255, 0, 0))
    break_ = False
    while True:
        window.fill((0, 191, 255))
        window.blit(text, (0, 0))
        window.blit(text2, (0, 40))
        pygame.display.update()
        if break_: break
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN) or (event.type == pygame.MOUSEBUTTONDOWN):
                break_ = True
                break

    pygame.quit()
    sys.exit(1)

loading.setValue('Loading dependencies...100% complete')
loading.draw()
time.sleep(0.5)
pygame.font.init()
loading_obj.done()
"""
----------------------------
| version: 9.5             |
| develop time: 2025-4-23  |
----------------------------
"""

############################################################
#init all the things----------------------------------------
############################################################
xticks_angle = -45
mode = 'DEG'
functions = ["sin", "cos", "tan", 'arcsin', "arccos", "arctan", "log", "ln", "√", 'min']
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_position(('data', 0.0))
ax.spines['bottom'].set_position(('data', 0.0))

plt.close('all')
matplotlib.use('wxagg')
plt.grid(True, linestyle="--", alpha=0.5)
usr_notice = UsrNotice(window, (0, 0), 1004, 610)
x = sympy.symbols('x')
y = sympy.symbols('y')
z = sympy.symbols('z')
mathtext = ''
font_path = 'fonts/JetBrainsMono-Light.ttf'
warning_text = pygwidgets.DisplayText(window, (0, 530), '', font_path, 20, 1004, backgroundColor=(0, 191, 255),
                                      height=31)
line1 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 16,
                     ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '=', 'C'],
                     window, 60, 60, 0, 92, 62, 0, font=font_path, font_size=18, callbacks=None)

line2 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 16,
                     ['(', ')', 'M', 'M+', 'Rad', 'Deg', 'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', '!',
                      'alog(x)', 'ln(x)', '(a)√(x)'], window, 60, 60, 0, 152, 62, 0, font=font_path, font_size=11,
                     callbacks=None)

line3 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 7,
                     ['.', 'e', 'π', '^', 'integral', 'double integral', 'triple integral']
                     , window, 120, 60, 0, 212, 124, 0, font=font_path, font_size=11, callbacks=None)

line4_1 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 3,
                       ['differential(s)', 'function image', 'data visualize'], window, 160, 60, 0, 272, 166,
                       0, font=font_path, font_size=14, callbacks=None)

line4_2 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 4,
                       ['M Clean', 'percent', 'simplify', 'solve'], window, 120, 60, 496, 272, 124, 0
                       , font=font_path, font_size=14, callbacks=None)

line5 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 8,
                     ['limit', 'clean memory', 'copy answer', 'data analyze', 'distribution', 'comparison', 'matrix',
                      'complex'], window, 120, 60, 0, 332, 124, 0, font=font_path,
                     font_size=14, callbacks=None)

line6 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 8,
                     ['vector', 'divisors', 'prime factors', 'GCD', '<-(answer)', '->(answer)', 'head(answer)',
                      'No-mouse:OFF'], window, 120, 60, 0, 392, 124, 0, font=font_path,
                     font_size=14, callbacks=None)
line7 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 5,
                     ['paste', 'user guide', 'A(n,m)', 'C(n,m)', 'copy formula'], window, 120, 60, 0, 452, 124, 0,
                     font=font_path,
                     font_size=14, callbacks=None)

answer = ''
backspace = pygwidgets.TextButton(window, (870, 212), 'backspace', 120, 60, textColor=(0, 0, 0), upColor=(90, 90, 150),
                                  overColor=(0, 50, 100), downColor=(20, 0, 80), fontName=font_path, fontSize=18)
science_mode = False
science = pygwidgets.TextButton(window, (620, 452), 'science:off', 120, 60, textColor=(0, 0, 0), upColor=(90, 90, 150),
                                  overColor=(0, 50, 100), downColor=(20, 0, 80), fontName=font_path, fontSize=16)

usr_showing_maths_texts = ''
text = pygwidgets.DisplayText(window, (0, 0), usr_showing_maths_texts, font_path, 60, 1004, backgroundColor=(255, 255, 255), height=90)
answertext = pygwidgets.DisplayText(window, (0, 570), '', font_path, 30, 1004, backgroundColor=(255, 255, 255),
                                    height=40)
left = 0
right = 0
no_mouse = False
MEMORY = ('', '')
point = True
matrix_saved_data, complex_saved_data, vector_saved_data = ({}, [], None), ({}, [], None), ({}, [], None)
func = 0
mode_text = pygwidgets.DisplayText(window, (970, 65), mode, textColor=(100, 100, 100), backgroundColor=(255, 255, 255),
                                   fontName=font_path)
draw_all()
pygame.display.update()
text_length_warned = False
answer_start_index = 0
pygame.key.set_repeat(200)
operator = True

###############################################################################################################
#main loop-----------------------------------------------------------------------------------------------------
###############################################################################################################
while True:
    mode_text.setValue(mode)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            ctrl = (keys[pygame.K_LCTRL]) or (keys[pygame.K_RCTRL])
            if ctrl and event.key == pygame.K_c:
                t = answertext.getValue()
                if t is None:
                    message_window.error('There is no answer to copy!')
                    continue
                pyperclip.copy(t)
                continue
            elif ctrl and event.key == pygame.K_v:
                content = pyperclip.paste()
                try:
                    content = float(content)
                    mathtext += str(content)
                    usr_showing_maths_texts += str(content)
                    continue
                except:
                    message_window.error('the content that you want to paste is:"' + str(
                        content) + '" ;which is not a number(only numbers is supported yet)')
                    continue
            if event.key == pygame.K_RETURN:
                #print(mathtext)
                try:
                    if mode == 'RAD':
                        text_ = Calculation(mathtext, 'RAD', science_mode)
                        if 'ERROR' in str(text_):
                            message_window.error(str(text_))
                        else:
                            answertext.setValue(text_)
                            answer = str(text_)
                    else:
                        text_ = Calculation(mathtext, 'DEG', science_mode)
                        # print(text_)
                        if 'ERROR' in str(text_):
                            message_window.error(str(text_))
                        else:
                            answertext.setValue(text_)
                            answer = str(text_)

                except Exception as e:
                    message_window.error('Invalid mathematical expression:' + str(usr_showing_maths_texts) + ',please recheck your input')
            elif event.key == pygame.K_LEFT:
                if len(answer) > 65:
                    # left move
                    _ = answer
                    if answer_start_index != 0:
                        answer_start_index -= 1
                    answertext.setValue(_[answer_start_index:66 + answer_start_index])
            elif event.key == pygame.K_RIGHT:
                if len(answer) > 65:
                    # right move
                    _ = answer
                    if answer_start_index + 65 < len(_):
                        answer_start_index += 1
                    answertext.setValue(_[answer_start_index:66 + answer_start_index])
            elif event.key == pygame.K_DELETE:
                usr_showing_maths_texts = ''
                mathtext = ''
                answer = ''
                point = True
                operator = True
            num = get_number_key(event)
            if num is not None:
                operator = False
                usr_showing_maths_texts += str(num)
                mathtext += str(num)
                continue
            symbol = get_calcu_symbol_key(event)
            if symbol is not None:
                if symbol == '+':
                    usr_showing_maths_texts += '+'
                    point = True
                    if left > right:  # 当前输入的是函数的参数
                        mathtext += '+'
                    else:
                        mathtext += ' + '  # 在[]外
                        func = 0
                    operator = True
                elif symbol == '-':
                    usr_showing_maths_texts += '-'
                    point = True
                    if left > right:  # 当前输入的是函数的参数
                        mathtext += '-'
                        operator = True
                    else:
                        if operator:  # 取相反数
                            mathtext += '-'
                            operator = False
                        else:
                            operator = True
                            mathtext += ' - '  # 在[]外
                        func = 0
                elif symbol == '*':
                    usr_showing_maths_texts += '*'
                    point = True
                    if left > right:  # 当前输入的是函数的参数
                        mathtext += '*'
                    else:
                        mathtext += ' * '  # 在[]外
                        func = 0
                    operator = True
                elif symbol == '/':
                    usr_showing_maths_texts += '/'
                    point = True
                    if left > right:  # 当前输入的是函数的参数
                        mathtext += '/'
                    else:
                        mathtext += ' / '  # 在[]外
                        func = 0
                    operator = True
                elif symbol == '.':
                    if point:
                        usr_showing_maths_texts += '.'
                        mathtext += '.'
                        point = False
                    else:
                        line3.Buttons[0].disable()
                elif symbol == '(':
                    usr_showing_maths_texts += '('
                    if not func:
                        if left > right:  # 当前输入的是函数的参数
                            mathtext += '('
                        else:
                            mathtext += ' ( '
                    else:
                        mathtext += '['
                        left += 1
                    operator = True
                elif symbol == ')':
                    usr_showing_maths_texts += ')'
                    if not func:
                        if left > right:  # 当前输入的是函数的参数
                            mathtext += ')'
                        else:
                            mathtext += ' ) '
                    else:
                        mathtext += ']'
                        right += 1
                        if left == right:  # means exit from present function
                            func = 0
                    operator = False
                elif symbol == '!':
                    mathtext += '!'
                    usr_showing_maths_texts += '!'
                    func = 1
                    operator = False
                elif symbol == '^':
                    point = True
                    usr_showing_maths_texts += '^'
                    if left > right:
                        mathtext += '^'
                    else:
                        mathtext += ' ^ '
                    operator = True
                else:
                    continue
            if event.key == pygame.K_BACKSPACE:
                usr_showing_maths_texts = usr_showing_maths_texts[0:-1]
                if len(mathtext) == 0:
                    operator = True
                    continue
                while mathtext[-1] == " ":
                    mathtext = mathtext[0:-1]
                if mathtext[-1] == ';':
                    mathtext = mathtext[0:-1]
                if mathtext[-1] == '[':
                    left -= 1
                elif mathtext[-1] == ']':
                    right -= 1
                mathtext = mathtext[0:-1]

                while (len(mathtext) != 0) and (mathtext[-1] == ' '):
                    mathtext = mathtext[0:-1]

                if len(mathtext) == 0:
                    operator = True
                _ = mathtext.split(' ')
                _ = [i for i in _ if i != '']
                if len(_) == 0:
                    operator = True
                elif len(_) == 1:
                    # no opposite allowed:if it is '-', then it's already opposite. if it is number, then no opposite allowed.
                    operator = False
                else:
                    if _[-1] == '-':
                        if _[-2] in '-+/*':
                            operator = False
                        elif _[-2] in '0123456789':
                            operator = True
                if any(a in mathtext.split(" ")[-1] for a in
                       functions):  # ["sin","cos","tan",'arcsin',"arccos","arctan","log","in","root"]
                    func = 1
        gui_math_text = convert_sqrt_expression(usr_showing_maths_texts)
        window.fill((0, 191, 255))
        if len(usr_showing_maths_texts) <= 32:
            text = pygwidgets.DisplayText(window, (0, 0), gui_math_text, font_path, 50, 1004, backgroundColor=(255, 255, 255),
                                          height=92)
        elif len(usr_showing_maths_texts) <= 42:
            text = pygwidgets.DisplayText(window, (0, 0), gui_math_text, font_path, 40, 1004, backgroundColor=(255, 255, 255),
                                          height=92)
        elif len(usr_showing_maths_texts) <= 55:
            text = pygwidgets.DisplayText(window, (0, 0), gui_math_text, font_path, 30, 1004, backgroundColor=(255, 255, 255),
                                          height=92)
        elif len(usr_showing_maths_texts) <= 112:
            # 双行显示
            text = pygwidgets.DisplayText(window, (0, 0), gui_math_text[0:56], font_path, 30, 1004,
                                          backgroundColor=(255, 255, 255),
                                          height=31)
            text2 = pygwidgets.DisplayText(window, (0, 31), gui_math_text[56:112], font_path, 30, 1004,
                                           backgroundColor=(255, 255, 255),
                                           height=61)
            text2.draw()
        else:
            text = pygwidgets.DisplayText(window, (0, 0), gui_math_text[0:56], font_path, 30, 1004,
                                          backgroundColor=(255, 255, 255),
                                          height=31)
            over = len(gui_math_text) - 165
            if len(gui_math_text) > 165 and not text_length_warned:
                message_window.warning(
                    "The length of the string that you input is longer than the max number(165):" + str(len(usr_showing_maths_texts)) +
                    ", suggesting canceling the formula into a shorter one, or the screen won't be able to show all characters.")
                text_length_warned = True
            if over <= 0:
                text_length_warned = False
                text.setValue(gui_math_text[0:56])
                text2 = pygwidgets.DisplayText(window, (0, 31), gui_math_text[56:112], font_path, 30, 1004,
                                               backgroundColor=(255, 255, 255),
                                               height=31)
                text3 = pygwidgets.DisplayText(window, (0, 62), gui_math_text[112:165], font_path, 30, 1004,
                                               backgroundColor=(255, 255, 255),
                                               height=30)
            else:
                text.setValue(gui_math_text[over:56 + over])
                text2 = pygwidgets.DisplayText(window, (0, 31), gui_math_text[56 + over:112 + over], font_path, 30, 1004,
                                               backgroundColor=(255, 255, 255),
                                               height=31)
                text3 = pygwidgets.DisplayText(window, (0, 62), gui_math_text[112 + over:165 + over], font_path, 30, 1004,
                                               backgroundColor=(255, 255, 255),
                                               height=31)
            text2.draw()
            text3.draw()

        if len(answer) > 65:
            #print('over')
            # the answer passes the display limit
            warning_text.setValue('The answer has ' + str(len(answer)) + ' digits, current showing:' + str(
                answer_start_index) + '~' + str(65 + answer_start_index))
            _ = answer
            answertext.setValue(_[answer_start_index:66 + answer_start_index])
        else:
            warning_text.setValue('')
        draw_all()
        event_proceeded = False

        for i in line1.Buttons:
            INDEX = line1.Buttons.index(i)
            if i.handleEvent(event):
                if INDEX < 10:  # 输入数字
                    usr_showing_maths_texts += str(INDEX)
                    mathtext += str(INDEX)
                    operator = False
                else:
                    if INDEX == 15:
                        usr_showing_maths_texts = ''
                        mathtext = ''
                        answer = ''
                        point = True
                        operator = True
                    elif INDEX == 10:
                        usr_showing_maths_texts += '+'
                        point = True
                        operator = True
                        if left > right:  # 当前输入的是函数的参数
                            mathtext += '+'
                        else:
                            mathtext += ' + '  # 在[]外
                            func = 0
                    elif INDEX == 11:
                        usr_showing_maths_texts += '-'
                        point = True
                        if left > right:  # 当前输入的是函数的参数
                            mathtext += '-'
                            operator = True
                        else:
                            if operator:  # 取相反数
                                mathtext += '-'
                                operator = False
                            else:
                                operator = True
                                mathtext += ' - '  # 在[]外
                            func = 0
                    elif INDEX == 12:
                        usr_showing_maths_texts += '*'
                        point = True
                        operator = True
                        if left > right:  # 当前输入的是函数的参数
                            mathtext += '*'
                        else:
                            mathtext += ' * '  # 在[]外
                            func = 0
                    elif INDEX == 13:
                        usr_showing_maths_texts += '/'
                        point = True
                        operator = True
                        if left > right:  # 当前输入的是函数的参数
                            mathtext += '/'
                        else:
                            mathtext += ' / '  # 在[]外
                            func = 0
                    elif INDEX == 14:
                        print(mathtext)
                        try:
                            if mode == 'RAD':
                                text_ = Calculation(mathtext, 'RAD', science_mode)
                                if 'ERROR' in str(text_):
                                    message_window.error(str(text_))
                                else:
                                    answertext.setValue(text_)
                                    answer = str(text_)
                            else:
                                text_ = Calculation(mathtext, 'DEG', science_mode)
                                #print(text_)
                                if 'ERROR' in str(text_):
                                    message_window.error(str(text_))
                                else:
                                    answertext.setValue(text_)
                                    answer = str(text_)

                        except Exception as e:
                            #raise e
                            message_window.error(str(e) + ',please recheck your input')
                    # print(mathtext)
                event_proceeded = True
                break

        if event_proceeded: continue

        for i in line2.Buttons:
            INDEX = line2.Buttons.index(i)
            if i.handleEvent(event):
                if INDEX == 0:
                    operator = True
                    usr_showing_maths_texts += '('
                    if not func:
                        if left > right:  # 当前输入的是函数的参数
                            mathtext += '('
                        else:
                            mathtext += ' ( '
                    else:
                        mathtext += '['
                        left += 1
                elif INDEX == 1:
                    operator = False
                    usr_showing_maths_texts += ')'
                    if not func:
                        if left > right:  # 当前输入的是函数的参数

                            mathtext += ')'
                        else:
                            mathtext += ' ) '
                    else:
                        mathtext += ']'
                        right += 1
                        if left == right:  # means exit from present function
                            func = 0
                elif INDEX == 2:
                    MEMORY = (usr_showing_maths_texts, mathtext)
                elif INDEX == 3:
                    usr_showing_maths_texts, mathtext = MEMORY
                elif INDEX == 4:
                    mode = 'RAD'
                elif INDEX == 5:
                    mode = 'DEG'
                elif INDEX == 6:
                    usr_showing_maths_texts += 'sin'
                    mathtext += 'sin;'
                    func = 1
                    operator = True
                elif INDEX == 7:
                    usr_showing_maths_texts += 'cos'
                    mathtext += 'cos;'
                    func = 1
                    operator = True
                elif INDEX == 8:
                    usr_showing_maths_texts += 'tan'
                    mathtext += 'tan;'
                    func = 1
                    operator = True
                elif INDEX == 9:
                    usr_showing_maths_texts += 'arcsin'
                    mathtext += 'arcsin;'
                    func = 1
                    operator = True
                elif INDEX == 10:
                    usr_showing_maths_texts += 'arccos'
                    mathtext += 'arccos;'
                    func = 1
                    operator = True
                elif INDEX == 11:
                    usr_showing_maths_texts += 'arctan'
                    mathtext += 'arctan;'
                    func = 1
                    operator = True
                elif INDEX == 12:
                    usr_showing_maths_texts += '!'
                    mathtext += '!'
                    func = 1
                    operator = False
                elif INDEX == 13:
                    usr_showing_maths_texts += 'log'
                    mathtext += 'log'
                    func = 1
                    operator = True
                elif INDEX == 14:
                    usr_showing_maths_texts += 'ln'
                    mathtext += 'ln'
                    func = 1
                    operator = True
                elif INDEX == 15:
                    usr_showing_maths_texts += '√'
                    mathtext += '√'
                    func = 1
                    operator = True
                event_proceeded = True
                break

        if event_proceeded: continue

        for i in line3.Buttons:
            INDEX = line3.Buttons.index(i)
            if i.handleEvent(event):
                if INDEX == 0:
                    if point:
                        usr_showing_maths_texts += '.'
                        mathtext += '.'
                        point = False
                    else:
                        i.disable()
                elif INDEX == 1:
                    point = False
                    usr_showing_maths_texts += 'e'
                    mathtext += str(math.e)
                elif INDEX == 2:
                    point = False
                    usr_showing_maths_texts += 'π'
                    mathtext += str(math.pi)
                elif INDEX == 3:
                    point = True
                    usr_showing_maths_texts += '^'
                    if left > right:
                        mathtext += '^'
                    else:
                        mathtext += ' ^ '
                    operator = True
                elif INDEX == 4: # single integral
                    formula = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                          'input you formula here( y/z = f(x /x,y)=', 'OK',
                                                          'CANCEL', backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0),
                                                          inputTextColor=(0, 0, 0))
                    if formula is None:
                        message_window.error('No formula is given')
                        continue
                    if not ('x' in formula or 'y' in formula):
                        message_window.error('You are not input a formula(contains "x" or/and "y"):'+str(formula))
                    else:
                        definite_integral = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'TYPE',
                                                                       'definite integral',
                                                                       'indefinite integral')
                        x = sympy.Symbol('x')
                        y = sympy.Symbol('y')
                        z = sympy.Symbol('z')

                        if not definite_integral:  # 不定积分
                            to_x = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                              'to', 'x  (dx)',
                                                              'y  (dy)')
                            if not to_x:  # 对y积分
                                Answer = sympy.integrate(sympy.sympify(formula), y)
                                answertext.setValue(Answer)
                                answer = str(Answer)
                            else:  # 对x积分
                                Answer = sympy.integrate(sympy.sympify(formula), x)
                                answertext.setValue(Answer)
                                answer = str(Answer)
                        else:
                            no_infinity = message_window.question('select integral type',
                                                                         'Do you want to do the normal integral(no Infinity included)')

                            to_x = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                  'to', 'x  (dx)',
                                                                  'y  (dy)')

                            # choose the max
                            if no_infinity:
                                integral_max = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                           'input maximum', 'OK',
                                                                           'cancel', backgroundColor=(90, 90, 150),
                                                                           promptTextColor=(0, 0, 0),
                                                                           inputTextColor=(0, 0, 0))
                            else:
                                have_infinity = message_window.question('select maximum type',
                                                                        'Do you want to input the normal max(no Infinity included)')
                                if have_infinity:
                                    positive_infinity = message_window.question('select maximum type',
                                                                                'Do you want to input a positive infinity(No means negative)')

                                    integral_max = sympy.oo if positive_infinity else -sympy.oo
                                else:
                                    integral_max = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                               'input maximum', 'OK',
                                                                               'cancel',
                                                                               backgroundColor=(90, 90, 150),
                                                                               promptTextColor=(0, 0, 0),
                                                                               inputTextColor=(0, 0, 0))
                            if integral_max is None:
                                message_window.error('No number is given!')
                                continue

                            # choose the min
                            if no_infinity:
                                integral_min = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                           'input minimum', 'OK',
                                                                           'cancel', backgroundColor=(90, 90, 150),
                                                                           promptTextColor=(0, 0, 0),
                                                                           inputTextColor=(0, 0, 0))
                            else:
                                have_infinity = message_window.question('select minium type',
                                                                        'Do you want to input the normal max(no Infinity included)')
                                if have_infinity:
                                    positive_infinity = message_window.question('select minium type',
                                                                                'Do you want to input a positive infinity(No means negative)')

                                    integral_min = sympy.oo if positive_infinity else -sympy.oo
                                else:
                                    integral_min = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                               'input minium', 'OK',
                                                                               'cancel',
                                                                               backgroundColor=(90, 90, 150),
                                                                               promptTextColor=(0, 0, 0),
                                                                               inputTextColor=(0, 0, 0))
                            if integral_min is None:
                                message_window.error('No numbers is given')
                                continue
                            if is_float(integral_min):integral_min = float(integral_min)
                            if is_float(integral_max):integral_max = float(integral_max)
                            try:
                                if not to_x:  # 对y积分
                                    Answer = sympy.integrate(sympy.sympify(formula), (y, integral_min, integral_max))
                                else:  # 对x积分
                                    Answer = sympy.integrate(sympy.sympify(formula), (x, integral_min, integral_max))

                                if isinstance(Answer, sympy.Integral):
                                    message_window.warning('Failed to get the symbol integral of:'+formula+', the system will return a numeric value')
                                    Answer = Answer.evalf()
                                    result, err = Answer.as_real_imag()
                                    if abs(err) > 0.1 * abs(result):
                                        message_window.warning('The answer is NOT reliable, the integral may be diverge')

                                answertext.setValue(str(Answer))
                                answer = str(Answer)
                            except Exception as e:
                                message_window.error('Failed to do the integral on formula:'+str(formula)+', because of the following error was occured:'+str(e))

                elif INDEX == 5: # double integral
                    formula = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                          'input you formula here( y/z = f(x /x,y)=', 'OK',
                                                          'CANCEL', backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0),
                                                          inputTextColor=(0, 0, 0))
                    if formula is None:
                        message_window.error('No formula is given')
                        continue
                    if not ('x' in formula or 'y' in formula):
                        message_window.error('You are not input a formula(contains "x" or/and "y"):'+str(formula))
                        continue

                    definite_integral = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'TYPE',
                                                                   'definite integral',
                                                                   'indefinite integral')
                    x = sympy.Symbol('x')
                    y = sympy.Symbol('y')
                    z = sympy.Symbol('z')
                    break_integral = False
                    if not definite_integral:  # 不定积分

                        to_x = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                          '(outer)to', 'x  (dx)',
                                                          'y  (dy)')
                        try:
                            if not to_x:  # 对y积分
                                # outer layer
                                Answer = sympy.integrate(sympy.sympify(formula), y)
                                to_x = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                  '(inner)to', 'x  (dx)',
                                                                  'y  (dy)')
                                if not to_x:  # 对y积分
                                    Answer = sympy.integrate(sympy.sympify(Answer), y)
                                else:  # 对x积分
                                    Answer = sympy.integrate(sympy.sympify(Answer), x)
                                answertext.setValue(Answer)
                                answer = str(Answer)

                            else:  # 对x积分
                                # outer layer
                                Answer = sympy.integrate(sympy.sympify(formula), x)
                                to_x = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                  '(inner)to', 'x  (dx)',
                                                                  'y  (dy)')
                                if not to_x:  # 对y积分
                                    Answer = sympy.integrate(sympy.sympify(Answer), y)
                                else:  # 对x积分
                                    Answer = sympy.integrate(sympy.sympify(Answer), x)
                                answertext.setValue(Answer)
                                answer = str(Answer)
                        except Exception as e:
                            message_window.error('Failed to do the integral on formula:'+str(formula)+', because of the following error was occurred:'+str(e))
                    else:
                        no_infinity = message_window.question('select integral type',
                                                              'Do you want to do the normal integral(no Infinity included)')
                        integral_list = []
                        for i in range(2):
                            to_x = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                              '(outer)to' if i == 0 else '(inner)to', 'x  (dx)',
                                                              'y  (dy)')
                            # choose the max
                            if no_infinity:
                                integral_max = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                           'input maximum', 'OK',
                                                                           'cancel', backgroundColor=(90, 90, 150),
                                                                           promptTextColor=(0, 0, 0),
                                                                           inputTextColor=(0, 0, 0))
                            else:
                                have_infinity = message_window.question('select maximum type',
                                                                        'Do you want to input the normal max(no Infinity included)')
                                if have_infinity:
                                    positive_infinity = message_window.question('select maximum type',
                                                                                'Do you want to input a positive infinity(No means negative)')

                                    integral_max = sympy.oo if positive_infinity else -sympy.oo
                                else:
                                    integral_max = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                               'input maximum', 'OK',
                                                                               'cancel',
                                                                               backgroundColor=(90, 90, 150),
                                                                               promptTextColor=(0, 0, 0),
                                                                               inputTextColor=(0, 0, 0))
                            if integral_max is None:
                                message_window.error('No numbers is given!')
                                break_integral = True
                                break

                            # choose the min
                            if no_infinity:
                                integral_min = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                           'input minimum', 'OK',
                                                                           'cancel', backgroundColor=(90, 90, 150),
                                                                           promptTextColor=(0, 0, 0),
                                                                           inputTextColor=(0, 0, 0))
                            else:
                                have_infinity = message_window.question('select minium type',
                                                                        'Do you want to input the normal max(no Infinity included)')
                                if have_infinity:
                                    positive_infinity = message_window.question('select minium type',
                                                                                'Do you want to input a positive infinity(No means negative)')

                                    integral_min = sympy.oo if positive_infinity else -sympy.oo
                                else:
                                    integral_min = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                               'input minium', 'OK',
                                                                               'cancel',
                                                                               backgroundColor=(90, 90, 150),
                                                                               promptTextColor=(0, 0, 0),
                                                                               inputTextColor=(0, 0, 0))
                            if integral_min is None:
                                message_window.error('No numbers is given')
                                break_integral = True
                                break
                            if is_float(integral_min):integral_min = float(integral_min)
                            if is_float(integral_max):integral_max = float(integral_max)
                            integral_list.append(x if to_x else y)
                            integral_list.append(integral_min)
                            integral_list.append(integral_max)

                        if break_integral:continue
                        try:
                            # the first(outer) layer of integral
                            if integral_list[0]:# to x
                                Answer = sympy.integrate(sympy.sympify(formula), (x, integral_list[1], integral_list[2]))
                            else: # to y
                                Answer = sympy.integrate(sympy.sympify(formula), (y, integral_list[1], integral_list[2]))

                            # the second(inner) layer of the integral
                            if integral_list[3]: # to x
                                Answer = sympy.integrate(sympy.sympify(Answer),
                                                             (x, integral_list[4], integral_list[5]))
                            else: # to y
                                Answer = sympy.integrate(sympy.sympify(Answer),
                                                             (y, integral_list[4], integral_list[5]))



                            if isinstance(Answer, sympy.Integral):
                                message_window.warning(
                                    'Failed to get the symbol integral of:' + formula + ', the system will return a numeric value')
                                Answer = Answer.evalf()
                                result, err = Answer.as_real_imag()
                                if abs(err) > 0.1 * abs(result):
                                    message_window.warning('The answer is NOT reliable, the integral may be diverge')
                            answertext.setValue(str(Answer))
                            answer = str(Answer)
                        except Exception as e:
                            message_window.error('Failed to do the integral on formula:' + str(
                                formula) + ', because of the following error was occurred:' + str(e))

                elif INDEX == 6: # triple integral
                    integrate_list = []
                    formula = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                          'input you formula here( y/z = f(x /x,y)=', 'OK',
                                                          'CANCEL', backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0),
                                                          inputTextColor=(0, 0, 0))
                    if formula is None:
                        message_window.error('No formula is given')
                        continue
                    if not ('x' in formula or 'y' in formula):
                        message_window.error('You are not input a formula(contains "x" or/and "y"):'+str(formula))
                        continue

                    definite_integral = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'TYPE',
                                                                   'definite integral',
                                                                   'indefinite integral')
                    x = sympy.Symbol('x')
                    y = sympy.Symbol('y')
                    z = sympy.Symbol('z')
                    break_integral = False
                    if not definite_integral:
                        for index_ in range(3):
                            to_x = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'to', 'x  (dx)',
                                                              'y  (dy)')
                            integrate_list.append(to_x)
                        try:
                            if integrate_list[0]:  # 对x积分
                                Answer = sympy.integrate(sympy.sympify(formula), x)
                            else:
                                Answer = sympy.integrate(sympy.sympify(formula), x)
                            for i in range(2):
                                if integrate_list[i + 1]:
                                    Answer = sympy.integrate(sympy.sympify(Answer), x)
                                else:
                                    Answer = sympy.integrate(sympy.sympify(Answer), y)
                            answertext.setValue(Answer)
                            answer = str(Answer)
                        except Exception as e:
                            message_window.error('Failed to do the integral on formula:' + str(
                                formula) + ', because of the following error was occurred:' + str(e))
                    else:
                        no_infinity = message_window.question('select integral type',
                                                              'Do you want to do the normal integral(no Infinity included)')
                        agreements = []
                        for index_ in range(3):

                            to_x = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'to', 'x  (dx)'
                                                              , 'y  (dy)')
                            integrate_list.append(to_x)
                            # choose the max
                            if no_infinity:
                                integral_max = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                           'input maximum', 'OK',
                                                                           'cancel', backgroundColor=(90, 90, 150),
                                                                           promptTextColor=(0, 0, 0),
                                                                           inputTextColor=(0, 0, 0))
                            else:
                                have_infinity = message_window.question('select maximum type',
                                                                        'Do you want to input the normal max(no Infinity included)')
                                if have_infinity:
                                    positive_infinity = message_window.question('select maximum type',
                                                                                'Do you want to input a positive infinity(No means negative)')

                                    integral_max = sympy.oo if positive_infinity else -sympy.oo
                                else:
                                    integral_max = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                               'input maximum', 'OK',
                                                                               'cancel',
                                                                               backgroundColor=(90, 90, 150),
                                                                               promptTextColor=(0, 0, 0),
                                                                               inputTextColor=(0, 0, 0))
                            if integral_max is None:
                                message_window.error('No numbers is given!')
                                break_integral = True
                                break
                            if is_float(integral_max):integral_max = float(integral_max)
                            agreements.append(integral_max)
                            # choose the min
                            if no_infinity:
                                integral_min = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                           'input minimum', 'OK',
                                                                           'cancel', backgroundColor=(90, 90, 150),
                                                                           promptTextColor=(0, 0, 0),
                                                                           inputTextColor=(0, 0, 0))
                            else:
                                have_infinity = message_window.question('select minium type',
                                                                        'Do you want to input the normal max(no Infinity included)')
                                if have_infinity:
                                    positive_infinity = message_window.question('select minium type',
                                                                                'Do you want to input a positive infinity(No means negative)')

                                    integral_min = sympy.oo if positive_infinity else -sympy.oo
                                else:
                                    integral_min = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                                               'input minium', 'OK',
                                                                               'cancel',
                                                                               backgroundColor=(90, 90, 150),
                                                                               promptTextColor=(0, 0, 0),
                                                                               inputTextColor=(0, 0, 0))
                            if integral_min is None:
                                message_window.error('No numbers is given')
                                break_integral = True
                                break
                            if is_float(integral_min): integral_min = float(integral_min)
                            agreements.append(integral_min)
                        if break_integral:continue
                        try:
                            Answer = sympy.integrate(sympy.sympify(formula), (agreements[0], agreements[2], agreements[1]))
                            if len(agreements) == 6:
                                for index_ in range(2):
                                    Answer = sympy.integrate(sympy.sympify(Answer),
                                                             (agreements[index_ + 2], agreements[index_ + 4], agreements[index_ + 3]))
                            else:
                                Answer = 'ERROR'
                            if isinstance(Answer, Integral):
                                message_window.warning(
                                    'Failed to get the symbol integral of:' + formula + ', the system will return a numeric value')
                                Answer = Answer.evalf()
                                result, err = Answer.as_real_imag()
                                if abs(err) > 0.1 * abs(result):
                                    message_window.warning('The answer is NOT reliable, the integral may be diverge')
                            answertext.setValue(Answer)
                            answer = str(Answer)
                        except Exception as e:
                            message_window.error('Failed to do the integral on formula:' + str(
                                formula) + ', because of the following error was occurred:' + str(e))
                event_proceeded = True
                break

        if event_proceeded: continue

        for i in line4_1.Buttons:
            INDEX = line4_1.Buttons.index(i)
            if i.handleEvent(event):
                if INDEX == 0:
                    formula = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                          'input you formula here( y/z = f(x[,y])=', 'OK',
                                                          'CANCEL', backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0),
                                                          inputTextColor=(0, 0, 0))
                    try:
                        if 'x' in formula:
                            pass
                    except TypeError:
                        continue
                    answertext.setValue('')
                    num = textNumberDialogEventProgressing(window, (200, 100, 800, 200),
                                                           'how many times do you want to differential at all', [], [],
                                                           'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0),
                                                           inputTextColor=(0, 0, 0))

                    if num == 0 or (num is None):
                        continue
                    break_ = False
                    Answer = None
                    for c2 in range(int(num)):
                        check = CheckBox(3, ['to x', 'to y', 'to z'], 1, window, clock, 300, 300, each_add_x=0,
                                         each_add_y=20, bkg_height_adj=100)
                        if len(check.clicked_choices) == 1:
                            check = str(check.clicked_choices[0])
                        else:
                            message_window.error('exit because of no choice selected')
                            break_ = True
                            break
                        x = sympy.symbols('x')
                        y = sympy.symbols('y')
                        z = sympy.symbols('z')
                        formula = sympy.sympify(formula)
                        if c2 == 0:
                            if check == '0':
                                Answer = formula.diff(x, 1)
                            elif check == '1':
                                Answer = formula.diff(y, 1)
                            elif check == '2':
                                Answer = formula.diff(z, 1)
                            else:
                                answertext.setValue('')
                                break
                        else:
                            if check == '0':
                                Answer = Answer.diff(x, 1)
                            elif check == '1':
                                Answer = Answer.diff(y, 1)
                            elif check == '2':
                                Answer = Answer.diff(z, 1)
                            else:
                                answertext.setValue('')
                                break
                    if not break_:
                        answertext.setValue(Answer)
                        answer = str(Answer)
                elif INDEX == 1:
                    plt.title('')
                    ploter = True
                    line_num = textNumberDialogEventProgressing(window, (200, 100, 800, 200),
                                                               'how many line(s) do you want to draw?', [], [], 'OK',
                                                               'CANCEL', backgroundColor=(90, 90, 150),
                                                                promptTextColor=(0, 0, 0),
                                                                inputTextColor=(0, 0, 0), allow_float=False,
                                                                allow_negative=False)

                    if line_num is None or line_num < 1:
                        continue
                    x1 = textNumberDialogEventProgressing(window, (200, 100, 800, 200),
                                                          'max x', [], [], 'OK',
                                                          'CANCEL', backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0),
                                                          inputTextColor=(0, 0, 0))
                    if x1 is None: message_window.error('no value is given');continue
                    x2 = textNumberDialogEventProgressing(window, (200, 100, 800, 200),
                                                          'min x', [], [], 'OK', 'CANCEL',
                                                          backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0),
                                                          inputTextColor=(0, 0, 0))
                    if x2 is None: message_window.error('no value is given');continue

                    set_ylim_manually = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'Do you want to set the y-limits manually', 'Yes'
                                                      , 'No')
                    if set_ylim_manually:
                        y1 = textNumberDialogEventProgressing(window, (200, 100, 800, 200),
                                                              'max y', [], [], 'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0),
                                                              inputTextColor=(0, 0, 0))
                        if y1 is None: message_window.error('no value is given');continue
                        y2 = textNumberDialogEventProgressing(window, (200, 100, 800, 200),
                                                              'min y', [], [], 'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0),
                                                              inputTextColor=(0, 0, 0))
                        if y2 is None: message_window.error('no value is given');continue

                    _x = np.linspace(float(x2), float(x1), 1000)
                    _xs = []
                    bar = windows_progress_bar(1000 * (int(line_num)), window, title='charting...', x=200, y=200, specific=False)

                    for c in range(int(line_num)):  # start drawing
                        formula = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                              'input you formula to draw here y = f(x) =', 'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0),
                                                              inputTextColor=(0, 0, 0))
                        try:
                            if 'x' in formula:
                                pass
                        except TypeError:
                            ploter = False
                            break
                        label = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                            'input you label', 'OK',
                                                            'CANCEL', backgroundColor=(90, 90, 150),
                                                            promptTextColor=(0, 0, 0),
                                                            inputTextColor=(0, 0, 0))
                        try:
                            if 'x' in label:
                                pass
                        except TypeError:
                            label = ''
                        Answer = sympy.sympify('(' + formula + ')-y')  # 对y求值
                        Formula = sympy.lambdify(sympy.symbols('x'), Answer, 'numpy')
                        _ys = []
                        _xs = []
                        for d, e in zip(_x, range(len(_x))):
                            _y = sympy.solve(Answer, y)  # 计算出合适的y值并加入列表中
                            x_value = d
                            _xs.append(x_value)
                            if len(_y) < 2:
                                y_val = _y[0].subs(x, d)
                                _ys.append(y_val)
                            else:
                                for index_ in range(len(_y)):
                                    y_val = _y[index_].subs(x, d)
                                    _ys.append(y_val)
                                    if index_ > 0:
                                        x_value = d
                                        _xs.append(x_value)
                            bar.update_time(e + 1 + c * 1000)
                            bar.update()
                        _ys = np.array(_ys)
                        _xs = np.array(_xs)
                        if label:
                            plt.plot(_xs, _ys, label=label)
                        else:
                            plt.plot(_xs, _ys)
                        if not set_ylim_manually:
                            y2 = float(np.min(_ys))
                            y1 = float(np.max(_ys))
                        plt.axis((x2, x1, y2, y1))  # initialize the board

                        plt.xlim(float(x2),float(x1))
                        plt.ylim(float(y2), float(y1))
                        xticks = np.linspace(float(x1), float(x2), 21)

                        xtick = []
                        for i in xticks:
                            if (abs(i) > 1000 or abs(i) < 0.001) and i != 0:
                                xtick.append('{:.4e}'.format(i))
                            else:
                                xtick.append(str(i)[0:5])
                        plt.xticks(ticks=xticks, labels=xtick, rotation=xticks_angle)
                        yticks = np.linspace(float(y1), float(y2), 21)
                        ytick = []
                        for i in yticks:
                            if abs(i) > 1000 or abs(i) < 0.001 and i != 0:
                                ytick.append('{:.4e}'.format(i))
                            else:
                                ytick.append(str(i)[0:5])
                        plt.yticks(ticks=yticks, labels=ytick)
                    if ploter:
                        plt.legend()  # 显示文本
                        plt.show()
                elif INDEX == 2:  # data visualize
                    visualize_2d = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                              'Select the type of visualize',
                                                              '2D', "3D")
                    if visualize_2d:
                        data_visualize_2d(window, clock)
                    else:
                        data_visualize_3d(window, clock)
                event_proceeded = True
                break

        if event_proceeded: continue

        for i in line4_2.Buttons:
            INDEX = line4_2.Buttons.index(i)
            if i.handleEvent(event):
                if INDEX == 0:
                    MEMORY = ('', '')
                elif INDEX == 1:
                    usr_showing_maths_texts += '%'
                    mathtext += '%'
                elif INDEX == 2:
                    formula = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                          'input the formula that you want to simplify', 'OK',
                                                          'CANCEL', backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0),
                                                          inputTextColor=(0, 0, 0))
                    if formula is not None:
                        try:
                            if '=' in formula:
                                message_window.error("Can't simplify a equation!!!")
                            simplified_formula = sympy.sympify(formula)
                            answertext.setValue(str(simplified_formula))
                            answer = str(simplified_formula)
                        except Exception as e:
                            message_window.error(
                                "Can't simplify the formula:" + formula + ", due to the Error:" + str(e))
                    else:
                        message_window.error("Failed to simplify due to an empty formula was given")
                elif INDEX == 3:
                    formula = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                          'input the formula(s) that you want to solve, '
                                                          'split with ";"',
                                                          'OK',
                                                          'CANCEL', backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0),
                                                          inputTextColor=(0, 0, 0))
                    if formula is not None:
                        all_formulas = formula.split(';')
                        all_formulas = [i for i in all_formulas if i is not None]
                        for current, index in zip(all_formulas, range(len(all_formulas))):
                            if '=' in current:
                                left_part, right_part = current.split('=')[0], current.split('=')[1]
                                all_formulas[index] = '(' + left_part + ')-(' + right_part + ')'
                        symbols = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                              'input the symbol(s) that you use in the formula:' + str(
                                                                  formula) + ',split with ";"',
                                                              'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0),
                                                              inputTextColor=(0, 0, 0))
                        symbols = symbols.split(';')
                        symbols = [i for i in symbols if i is not None]
                        try:
                            symbols_used = [sympy.Symbol(i) for i in symbols]
                            simplified_formula = [sympy.sympify(i) for i in all_formulas]
                            answers = sympy.solve(simplified_formula, symbols_used, dict=True)
                            answertext.setValue(str(answers))
                            answer = str(answers)
                        except Exception as e:
                            message_window.error(
                                "Can't solve the formula:" + formula + ", due to the Error:" + str(e))
                    else:
                        message_window.error("Failed to solve the formula due to an empty formula was given")
                event_proceeded = True
                break

        if event_proceeded: continue

        for i in line5.Buttons:
            INDEX = line5.Buttons.index(i)
            if i.handleEvent(event):
                if INDEX == 0:
                    formula = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                          'input the formula that you want to get the limit', 'OK',
                                                          'CANCEL', backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0),
                                                          inputTextColor=(0, 0, 0))
                    if formula is not None:
                        if '=' in formula:
                            message_window.error("Can't get the limit of the equation:" + str(formula))
                            continue
                        symbols = pyghelpers.textAnswerDialog(window, (200, 100, 800, 200),
                                                              'input the symbol that you use in the formula:' + str(
                                                                  formula) + ',only ONE symbol',
                                                              'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0),
                                                              inputTextColor=(0, 0, 0))
                        symbols = [sympy.Symbol(i) for i in symbols.split(';') if i is not None]
                        limit = 'None'
                        try:
                            no_infinity_limits = message_window.question('select limit type',
                                                                         'Do you want to do the normal limit(no Infinity included)')
                            if no_infinity_limits:
                                limit = textNumberDialogEventProgressing(window, (200, 100, 800, 200),
                                                                         'input the limit that you use in the formula:' + str(
                                                                             formula) + '(' + str(symbols) + ')',
                                                                         [], [], 'OK',
                                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                                         promptTextColor=(0, 0, 0),
                                                                         inputTextColor=(0, 0, 0))
                                if limit is None:
                                    message_window.error('no limit is given')
                                    break
                                direction = CheckBox(3, ['+', '-', '+/-'], 1, window, clock, first_x=120, first_y=30,
                                                     each_add_x=0, each_add_y=20)

                                simplified_formula = sympy.sympify(formula)
                                if type(direction.clicked_choices) == str or direction.clicked_choices == []:
                                    answers = sympy.limit(simplified_formula, symbols, limit)
                                else:
                                    answers = sympy.limit(simplified_formula, symbols, limit,
                                                          ['+', '-', '+-'][direction.clicked_choices[0]])
                            else:
                                pos_inf = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                     'What infinity do you want?',
                                                                     'Postive(+) Infinity',
                                                                     "Negative(-) Infinity")
                                simplified_formula = sympy.sympify(formula)
                                if pos_inf:
                                    answers = sympy.limit(simplified_formula, symbols, sympy.oo)
                                else:
                                    answers = sympy.limit(simplified_formula, symbols, -sympy.oo)

                            answer = str(answers)
                            if answer == 'oo':
                                answer = 'infinity'
                            elif answer == '-oo':
                                answer = 'negative infinity'
                            elif answer == 'zoo':
                                answer = 'The limit does not exist'
                            answertext.setValue(answer)
                        except Exception as e:
                            message_window.error(
                                "Can't get the limit when" + str(symbols) + " limits to " + str(
                                    limit) + "the formula:" + formula + ", due to the Error:" + str(e))
                    else:
                        message_window.error("Failed to get the limit of the formula due to an empty formula was given")
                elif INDEX == 1:
                    MEMORY = ('', '')
                elif INDEX == 2:
                    pyperclip.copy(answer)
                elif INDEX == 3:
                    data_analyze(window, clock)
                elif INDEX == 4:
                    data_distribution(window, clock)
                elif INDEX == 5:
                    data_comparison(window, clock)
                elif INDEX == 6:
                    matrix_shower = MatrixUi(window, clock, (0, 0), 1004, 610, all_data=matrix_saved_data)
                    matrix_saved_data = matrix_shower.draw()
                elif INDEX == 7:
                    complex_shower = ComplexUi(window, clock, (0, 0), 1004, 610, all_data=complex_saved_data,
                                               no_mouse=no_mouse)
                    complex_saved_data = complex_shower.draw()
                event_proceeded = True
                break

        if event_proceeded: continue

        for i in line6.Buttons:
            if i.handleEvent(event):
                event_proceeded = True
                INDEX = line6.Buttons.index(i)
                if INDEX == 0:
                    vector_shower = VectorUi(window, clock, (0, 0), 1004, 610, all_data=vector_saved_data,
                                             no_mouse=no_mouse)
                    vector_saved_data = vector_shower.draw()
                elif INDEX == 1:
                    num = textNumberDialogEventProgressing(window, (0, 0, 1004, 190),
                                                           'input the number that you want to get the divisors', [], [],
                                                           'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                           allow_float=False, allow_negative=False)
                    if num is None:
                        message_window.error('exit because of empty input')
                        break
                    answertext.setValue(str(sympy.divisors(num)))
                elif INDEX == 2:
                    num = textNumberDialogEventProgressing(window, (0, 0, 1004, 190),
                                                           'input the number that you want to get the prime factors',
                                                           [], [], 'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                           allow_float=False, allow_negative=False)
                    if num is None:
                        message_window.error('exit because of empty input')
                        break
                    if num == 0:
                        message_window.error('can only get the prime factors of NONE ZERO integers')
                        break
                    answertext.setValue(str(sympy.factorint(num)))
                elif INDEX == 3:
                    num = textNumberDialogEventProgressing(window, (0, 0, 1004, 190),
                                                           'input the first number that you want to get the GCD', [],
                                                           [], 'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                           allow_float=False, allow_negative=False)
                    if num is None:
                        message_window.error('exit because of empty input')
                        break
                    if num == 0:
                        message_window.error('can only get the GCD of NONE ZERO integers')
                        break
                    num2 = textNumberDialogEventProgressing(window, (0, 0, 1004, 190),
                                                            'input the second number that you want to get the GCD', [],
                                                            [], 'OK',
                                                            'CANCEL', backgroundColor=(90, 90, 150),
                                                            promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                            allow_float=False, allow_negative=False)
                    if num2 is None:
                        message_window.error('exit because of empty input')
                        break
                    if num2 == 0:
                        message_window.error('can only get the GCD of NONE ZERO integers')
                        break
                    answertext.setValue(str(sympy.gcd(num, num2)))
                elif INDEX == 4:
                    if len(answer) > 65:
                        # left move
                        _ = answer
                        if answer_start_index != 0:
                            answer_start_index -= 1
                        answertext.setValue(_[answer_start_index:66 + answer_start_index])
                elif INDEX == 5:
                    if len(answer) > 65:
                        # right move
                        _ = answer
                        if answer_start_index + 65 < len(_):
                            answer_start_index += 1
                        answertext.setValue(_[answer_start_index:66 + answer_start_index])
                elif INDEX == 6:
                    answer_start_index = 0
                elif INDEX == 7:
                    no_mouse = not no_mouse
                    line6 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 8,
                                         ['vector', 'divisors', 'prime factors', 'GCD', '<-(answer)', '->(answer)',
                                          'head(answer)', 'No-mouse:ON' if no_mouse else 'No-mouse:OFF'], window, 120,
                                         60, 0, 392, 124, 0,
                                         font=font_path,
                                         font_size=14, callbacks=None)
        if event_proceeded: continue

        for i in line7.Buttons:
            if i.handleEvent(event):
                event_proceeded = True
                INDEX = line7.Buttons.index(i)

                if INDEX == 0:
                    content = pyperclip.paste()
                    try:
                        content = float(content)
                        mathtext += str(content)
                        usr_showing_maths_texts += str(content)
                    except:
                        message_window.error('the content that you want to paste is:"' + str(
                            content) + '" ;which is not a number(only numbers is supported yet)')
                elif INDEX == 1:
                    usr_notice.draw()
                elif INDEX == 2:
                    #A(n, m)
                    n = textNumberDialogEventProgressing(window, (0, 0, 1004, 190), 'input the number "n"', [], [],
                                                         'OK',
                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                         promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                         allow_float=False, allow_negative=False)
                    if n is None: message_window.error("No inputs is given");break
                    m = textNumberDialogEventProgressing(window, (0, 0, 1004, 190), 'input the number "m"', [], [],
                                                         'OK',
                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                         promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                         allow_float=False, allow_negative=False)
                    if m is None: message_window.error("No inputs is given");break
                    if not n > m: message_window.error(
                        "n(" + str(n) + ") should be bigger than m(" + str(m) + ")!");break
                    answertext.setValue(str(scipy.special.perm(n, m)))
                    answer = str(scipy.special.perm(n, m))
                elif INDEX == 3:
                    #C(n, m)
                    n = textNumberDialogEventProgressing(window, (0, 0, 1004, 190), 'input the number "n"', [], [],
                                                         'OK',
                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                         promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                         allow_float=False, allow_negative=False)
                    if n is None: message_window.error("No inputs is given");break
                    m = textNumberDialogEventProgressing(window, (0, 0, 1004, 190), 'input the number "m"', [], [],
                                                         'OK',
                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                         promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                         allow_float=False, allow_negative=False)
                    if m is None: message_window.error("No inputs is given");break
                    if not n > m: message_window.error(
                        "n(" + str(n) + ") should be bigger than m(" + str(m) + ")!");break

                    answertext.setValue(str(math.comb(n, m)))
                    answer = str(math.comb(n, m))
                elif INDEX == 4:
                    pyperclip.copy(usr_showing_maths_texts)

        if science.handleEvent(event):
            science_mode = not science_mode
            science = pygwidgets.TextButton(window, (620, 452), 'science:' + ('on' if science_mode else 'off'), 120, 60,
                                            textColor=(0, 0, 0), upColor=(90, 90, 150),
                                            overColor=(0, 50, 100), downColor=(20, 0, 80), fontName=font_path,
                                            fontSize=16)

        if backspace.handleEvent(event):
            usr_showing_maths_texts = usr_showing_maths_texts[0:-1]
            if len(mathtext) == 0:
                continue
            while mathtext[-1] == " ":
                mathtext = mathtext[0:-1]
            if mathtext[-1] == ';':
                mathtext = mathtext[0:-1]
            if mathtext[-1] == '[':
                left -= 1
            elif mathtext[-1] == ']':
                right -= 1
            mathtext = mathtext[0:-1]
            while mathtext[-1] == ' ':
                mathtext = mathtext[0:-1]
            _ = mathtext.split(' ')
            if len(_) == 0:
                operator = True
            elif len(_) == 1:
                #no opposite allowed:if it is '-', then it's already opposite. if it is number, then no opposite allowed.
                operator = False
            else:
                if _[-1] == '-':
                    if _[-2] in '-+/*':
                        operator = False
                    elif _[-2] in '0123456789':
                        operator = True
            if any(a in mathtext.split(" ")[-1] for a in
                   functions):  # ["sin","cos","tan",'arcsin',"arccos","arctan","log","in","root"]
                func = 1

    if point:
        line3.Buttons[0].enable()
    else:
        line3.Buttons[0].disable()
    pygame.display.update()
    clock.tick(60)
