#https://blog.csdn.net/weixin_33755557/article/details/89592127

import matplotlib
matplotlib.use('WxAgg')
import pygame
import pygwidgets
import pyghelpers
from pygame.locals import *
from statistics import Message_window
message_window = Message_window()
from ExcleMagr import ExcelMgr
import traceback

import matplotlib
import matplotlib.pyplot as plt
import pyperclip

matplotlib.use('WXagg')
import pyghelpers
import sympy
import numpy

from math import log2, sqrt, pi
from ExcleMagr import ExcelMgr
from checkbox import *
from EventPyghelpers import textAnswerDialogEventProgressing, textYesNoDialogEventProgressing, textNumberDialogEventProgressing
from TableViewer.Table import WindowListViewer
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statistics import loading_data


def load_matrix(comments='', data_collecting_method=True, req: tuple[int, int] = None):
    global message_window
    if data_collecting_method:
        message_window.browser("Choose an Excel file for the matrix's source"+comments, [('EXCEL files', '.xlsx')])
        file_name = message_window.file_name
        if file_name == '':
            message_window.error('Failed to continue because of empty filename was given')
            return
        try:
            file = ExcelMgr(file_name)
        except Exception as e:
            message_window.error(str(e))
            return
        file_data = file.data
        list_preview = WindowListViewer(file_data, (1004, 410), window, (0, 200))
        choice = pyghelpers.textYesNoDialog(window, (0, 300, 600, 300), 'how do you want to collect data' + comments,
                                            "by line(----)", 'by column(| | |)')

        arrange_start = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input starting arrange number',
                                                         [list_preview.draw], [list_preview.handle_event], 'OK',
                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                         promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                         allow_float=False, allow_negative=False)

        if arrange_start is None:
            message_window.error('no inputs is given')
            return
        arrange_end = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input ending arrange number(included)',
                                                       [list_preview.draw], [list_preview.handle_event], 'OK',
                                                       'CANCEL', backgroundColor=(90, 90, 150),
                                                       promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                       allow_float=False, allow_negative=False)

        if arrange_end is None:
            message_window.error('no inputs is given')
            return

        column_start = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input starting column number',
                                                        [list_preview.draw], [list_preview.handle_event], 'OK',
                                                        'CANCEL', backgroundColor=(90, 90, 150),
                                                        promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                        allow_float=False, allow_negative=False)

        if column_start is None:
            message_window.error('no inputs is given')
            return
        column_end = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input ending column number(included)',
                                                      [list_preview.draw], [list_preview.handle_event], 'OK',
                                                      'CANCEL', backgroundColor=(90, 90, 150),
                                                      promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0),
                                                      allow_float=False, allow_negative=False)

        if column_end is None:
            message_window.error('no inputs is given')
            return

        try:
            if not choice:  ####by column ################################################################################
                file_data = [curr_line[column_start:column_end + 1] for curr_line in file_data]
                array = np.array(file_data)
                array = np.transpose(array)
                array = array.tolist()
                data = []
                for line in array:
                    data.append(line[arrange_start:arrange_end + 1])

            else:  ##### by line ################################################################################
                file_data = file_data[arrange_start:arrange_end + 1]
                data = []
                for line in file_data:
                    data.append(line[column_start:column_end + 1])
            return data
        except Exception as e:
            message_window.error(str(e))
            return
    else:
        if req is None:
            return
        x, y = req
        data = []
        for i in range(y):
            curr_data = pyghelpers.textAnswerDialog(window, (200, 100, 500, 200),
                                                    "input you line of data split each other with ';', num is "+str(x),
                                                    'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0),
                                                    inputTextColor=(0, 0, 0))
            if curr_data is None:
                message_window.error('No line of data is given.Quit.')
                return
            curr_data = curr_data.split(";")
            if len(curr_data) != x:
                message_window.error('Expect '+str(x)+' items,got '+str(len(curr_data))+' item(s) instead.')
                return
            for j in curr_data:
                try:
                    float(j)
                except:
                    message_window.error('You are not input a number:'+str(j))
                    return
            data.append(curr_data)
        return data


def data_visualize_3d(window, clock):
    axs = []
    fig = plt.figure()

    data_collecting_method = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect data',
                                                        '.xlsx file', "by inputting the data manually")
    many_charts = pyghelpers.textYesNoDialog(window, (0, 300, 600, 300),
                                             'How many charts of each type do you want to draw',
                                             'many', "only one each type")
    try:
        charting_type_selector = CheckBox(8, ['line plots', 'scatter plots', 'wireframe', 'surface',
                                              'tri-surface(Not recommended)',
                                              'bar plots', 'quivers', 'contour'], 8,
                                          window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30,
                                          buttons_adjust_length=0, background_color=(90, 90, 150))
        if type(charting_type_selector.clicked_choices) == str:
            return
        elif len(charting_type_selector.clicked_choices) == 0:
            choice_ = message_window.question("you didn't choice any type of charts, do you want to exit?")
            if not choice_:
                return data_visualize_3d(window, clock)
            else:
                return
        file_data = None
        if data_collecting_method:
            # preload the data's file
            message_window.browser("Choose an Excel file for the data's source", [('EXCEL files', '.xlsx')])
            file_name = message_window.file_name
            if file_name == '':
                message_window.error("failed to process because of empty file name.")
                file_data = None
            else:
                try:
                    file = ExcelMgr(file_name)
                    file_data = file.data
                except Exception as e:
                    message_window.error('Failed to preload data because of error:' + str(e))
                    file_data = None
            refresh_data = pyghelpers.textYesNoDialog(window, (0, 300, 600, 300),
                                                      'Do you want to refresh the data after each chart?',
                                                      'yes', "no")
        else:
            refresh_data = True

        chart_choices = []
        if many_charts:
            for charting_type_selector in charting_type_selector.clicked_choices:
                num = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'How many ' +
                                                  ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                                   'bar plots', 'quivers'][
                                                      charting_type_selector] + ' charts do you want to draw?',
                                                  'OK',
                                                  'CANCEL', backgroundColor=(90, 90, 150),
                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                try:
                    num = int(num)
                except Exception:
                    message_window.error("Can't turn " + str(num) + ' into an integer, terminate.')
                    return
                if num < 0:
                    message_window.error("You can't draw negative charts!Terminate.")
                    return
                else:
                    for i in range(num):
                        chart_choices.append(charting_type_selector)
        else:
            chart_choices = charting_type_selector.clicked_choices
        axs.append(fig.add_subplot(projection='3d'))
        x_label = pyghelpers.textAnswerDialog(window, (0, 300, 1004, 300),
                                                            'Insert X label',
                                                            'OK', "Cancel")
        axs[-1].set_xlabel(x_label if x_label is not None else 'x')
        y_label = pyghelpers.textAnswerDialog(window, (0, 300, 1004, 300),
                                              'Insert Y label',
                                              'OK', "Cancel")
        axs[-1].set_ylabel(y_label if y_label is not None else 'y')
        z_label = pyghelpers.textAnswerDialog(window, (0, 300, 1004, 300),
                                              'Insert Z label',
                                              'OK', "Cancel")
        axs[-1].set_zlabel(z_label if z_label is not None else 'z')
        index = 0
        for curr_type in chart_choices:
            if curr_type in [0, 1]:
                x_data = loading_data(data_collecting_method, window, 'for x:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data, file_data=file_data)
                if x_data is None:message_window.error('No x data is selected!, skip this draw');continue
                y_data = loading_data(data_collecting_method, window, 'for x:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data, file_data=file_data)
                if y_data is None: message_window.error('No y data is selected!, skip this draw');continue
                z_data = loading_data(data_collecting_method, window, 'for x:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data, file_data=file_data)
                if z_data is None: message_window.error('No z data is selected!, skip this draw');continue

                if not (len(x_data) == len(y_data) == len(z_data)):
                    message_window.error('The three datas do not have the same size:' + str(len(x_data)) + ',' + str(
                        len(y_data)) + ',' + str(len(z_data)))
                    return
                # draw
                if curr_type == 0: # line plots
                    axs[-1].plot(np.array(x_data), np.array(y_data), np.array(z_data))
                elif curr_type == 1:# scatter plots
                    axs[-1].scatter(x_data, y_data, z_data)
            elif curr_type in [2, 3, 4, 7]:
                x_data = loading_data(data_collecting_method, window, 'for x:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data,
                                      file_data=file_data)
                if x_data is None: message_window.error('No x data is selected!Skip this draw');continue
                y_data = loading_data(data_collecting_method, window, 'for y:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data,
                                      file_data=file_data)
                if y_data is None: message_window.error('No y data is selected!Skip this draw');continue
                z_data = load_matrix(comments='z[shape:('+str(len(x_data))+','+str(len(y_data))+')]', data_collecting_method=data_collecting_method,
                                     req=(len(x_data), len(y_data)))
                if z_data is None:
                    message_window.error('No z data is selected!Skip this draw');continue
                if len(z_data[0]) != len(x_data) or len(z_data) != len(y_data):
                    message_window.error('got z data in shape:('+str(len(z_data[0]))+','+str(len(z_data))+'),expect:('+str(len(x_data))+','+str(len(y_data))+'),Skip this draw')
                    continue

                z_data = np.array(z_data)
                x_data, y_data = np.meshgrid(np.array(x_data), np.array(y_data))

                if curr_type in [2, 3, 7]:
                    if curr_type == 2:
                        axs[-1].plot_wireframe(x_data, y_data, z_data)
                    elif curr_type == 3:
                        try:
                            axs[-1].plot_surface(x_data, y_data, z_data)
                        except MemoryError:
                            message_window.error("The memory of the system is not enough for the calculation!Consider closing other apps, run smaller data sets or change a computer.If you tried this but nothing works, the problem is out of Coc's control.Skip this draw")
                            continue
                    elif curr_type == 7:
                        draw_colour_bar = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                            'how do you want to draw the colour bar',
                                                                            'Yes',
                                                                            "No")
                        try:
                            surf = axs[-1].contour(x_data, y_data, z_data)
                        except:
                            z_data += np.random.normal(0, 1e-8, z_data.shape)

                            try:
                                surf = axs[-1].contour(x_data, y_data, z_data)
                                if draw_colour_bar:
                                    fig.colorbar(surf, ax=axs[-1], shrink=0.5)
                            except Exception as e:
                                message_window.error('Failed to draw the contour with Error:'+str(e)+',skip this draw')
                                continue
                        if draw_colour_bar:
                            fig.colorbar(surf, ax=axs[-1], shrink=0.5)
                else:
                    x_data = x_data.flatten()
                    y_data = y_data.flatten()
                    z_data = z_data.flatten()
                    try:
                        axs[-1].plot_trisurf(x_data, y_data, z_data)
                    except RuntimeError:
                        #三角剖分失败
                        message_window.warning('Failed to do triangulation calculation, retrying')
                        x_data += np.random.normal(0, 1e-8, x_data.shape)
                        y_data += np.random.normal(0, 1e-8, y_data.shape)
                        points = np.column_stack((x_data, y_data))
                        unique_points = np.unique(points, axis=0)
                        x_data, y_data = unique_points[:, 0], unique_points[:, 1]

                        try:
                            axs[-1].plot_trisurf(x_data, y_data, z_data)
                        except:
                            Skip = message_window.question(question='Failed to draw the tri-surface.Do you want to use plot_surface,wire frame(Choose no), or just skip(Choose yes)?', title='Skip?')
                            if Skip:continue
                            else:
                                surface = message_window.question('Select a type', 'Do you want to use plot_surface(Choose yes) or plot_wireframe(Choose no)')
                                if surface:
                                    try:
                                        axs[-1].plot_surface(x_data, y_data, z_data)
                                    except MemoryError:
                                        message_window.error("The memory of the system is not enough for the calculation!Consider closing other apps, run smaller data sets or change a computer.If you tried this but nothing works, the problem is out of Coc's control.Skip this draw")
                                        continue
                                else:
                                    axs[-1].plot_wireframe(x_data, y_data, z_data)

                    except MemoryError:
                        message_window.error("The memory of the system is not enough for the calculation!Consider closing other apps, run smaller data sets or change a computer.If you tried this but nothing works, the problem is out of Coc's control.Skip this draw")
                        continue
                    except:
                        message_window.error('Unexpected error, skip this draw')

            elif curr_type == 5:
                x_data = loading_data(data_collecting_method, window, 'for x data of the bar', reload_data=refresh_data,
                                      file_data=file_data)
                if x_data is None: message_window.error('No x data is selected!, skip this draw');continue
                y_data = loading_data(data_collecting_method, window, 'for y data of the bar', reload_data=refresh_data,
                                      file_data=file_data)
                if y_data is None: message_window.error('No y data is selected!, skip this draw');continue
                z_data = load_matrix('for the data part',data_collecting_method=data_collecting_method, req=(len(x_data), len(y_data)))
                if z_data is None:
                    message_window.error('No value is selected!, skip this draw');continue
                Index = 0
                for y in y_data:
                    axs[-1].bar(x_data, z_data[Index], y, zdir='y')
                    Index += 1



            elif curr_type == 6:
                x_data = loading_data(data_collecting_method, window, 'for x:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data,
                                      file_data=file_data)
                if x_data is None: message_window.error('No x data is selected!');continue
                y_data = loading_data(data_collecting_method, window, 'for y:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data,
                                      file_data=file_data)
                if y_data is None: message_window.error('No y data is selected!');continue
                z_data = loading_data(data_collecting_method, window, 'for z:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data,
                                      file_data=file_data)
                if z_data is None: message_window.error('No z data is selected!');continue
                if not (len(x_data) == len(y_data) == len(z_data)):
                    message_window.error("Dimensions don't match:"+str(len(x_data))+','+str(y_data)+','+str(z_data))

                u_data = loading_data(data_collecting_method, window, 'for u:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data,
                                      file_data=file_data)
                if u_data is None: message_window.error('No u data is selected!');continue
                v_data = loading_data(data_collecting_method, window, 'for v:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data,
                                      file_data=file_data)
                if v_data is None: message_window.error('No v data is selected!');continue
                w_data = loading_data(data_collecting_method, window, 'for z:' +
                                      ['line plots', 'scatter plots', 'wireframe', 'surface', 'tri-surface',
                                       'bar plots', 'quivers', 'contour'][curr_type], reload_data=refresh_data,
                                      file_data=file_data)
                if w_data is None: message_window.error('No w data is selected!');continue

                if not (len(x_data) == len(u_data) == len(v_data) == len(w_data)):
                    message_window.error("Dimensions don't match:"+str(len(x_data))+','+str(len(y_data))+','+str(len(z_data))+','+str(u_data)+','+str(v_data)+','+str(w_data))

                Index = 0
                for i in range(len(x_data)):
                    axs[-1].quiver(x_data[Index], y_data[Index], z_data[Index], u_data[Index], v_data[Index], w_data[Index])
                    Index += 1


            if index != (len(chart_choices)-2):
                if many_charts:
                    axs.append(fig.add_subplot(projection='3d'))
                    x_label = pyghelpers.textAnswerDialog(window, (0, 300, 1004, 300),
                                                          'Insert X label',
                                                          'OK', "Cancel")
                    axs[-1].set_xlabel(x_label if x_label is not None else 'x')
                    y_label = pyghelpers.textAnswerDialog(window, (0, 300, 1004, 300),
                                                          'Insert Y label',
                                                          'OK', "Cancel")
                    axs[-1].set_ylabel(y_label if y_label is not None else 'y')
                    z_label = pyghelpers.textAnswerDialog(window, (0, 300, 1004, 300),
                                                          'Insert Z label',
                                                          'OK', "Cancel")
                    axs[-1].set_zlabel(z_label if z_label is not None else 'z')
            if refresh_data:
                message_window.browser("Choose an Excel file for the refresh data's source", [('EXCEL files', '.xlsx')])
                file_name = message_window.file_name
                if file_name == '':
                    message_window.error("failed to process because of empty file name")
                    return
                try:
                    file = ExcelMgr(file_name)
                    file_data = file.data
                except Exception as e:
                    message_window.error('Failed to load data because of error:' + str(e))
                    file_data = None
            index += 1



    except Exception as e:
        message_window.error('Failed to paint because of error:'+str(e))


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1004, 610), DOUBLEBUF)
    window.fill((0, 191, 255))
    data_visualize_3d(window, clock)