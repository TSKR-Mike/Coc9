import tkinter as tk
import traceback
from tkinter import filedialog, messagebox

import matplotlib
import matplotlib.pyplot as plt
import pyperclip

matplotlib.use('WXagg')
import pyghelpers
import sympy
import sys
from math import log2, sqrt, pi
from ExcleMagr import ExcelMgr
from checkbox import *
from EventPyghelpers import textAnswerDialogEventProgressing, textYesNoDialogEventProgressing, textNumberDialogEventProgressing
from TableViewer.Table import WindowListViewer
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

def covariance(data1, data2):
    return np.cov(data1, data2)

def correlation(data1, data2):
    return np.corrcoef(data1, data2)[0, 1]

def kurtosis(data):
    return stats.kurtosis(data)

def skew(data):
    return stats.skew(data)

def percentile(data, percent):
    return np.percentile(data, percent)

def range_ptp(data):
    return np.ptp(data)

def mean(data):
    return np.mean(data)#平均值

def max(data):
    return np.max(data)#最大值

def min(data):
    return np.min(data)#最小值

def median(data):
    return np.median(data)#中位数

def mode(data):
    return stats.mode(data)#众数

def variance(data):
    return np.var(data)#方差

def standard_deviation(data):
    return np.std(data)#标准差

def moving_average(data, window_size):
    # 计算移动平均
    return [sum(data[i:i+window_size])/window_size for i in range(len(data)-window_size+1)]

def EWMA(data, alpha):
    # 计算指数加权移动平均（EWMA）
    ewma = [data[0]]
    for i in range(1, len(data)):
        ewma.append(alpha * data[i] + (1 - alpha) * ewma[-1])
    return ewma

def z_scores(data):
    # 计算列表元素的Z分数（标准分数）
    mean = np.mean(data)
    std_dev = np.std(data)
    return [(x - mean) / std_dev for x in data]

def CumulativeDistributionFunction(data):
    # 计算列表数据的累积密度函数（Cumulative Distribution Function, CDF）
    sorted_data = sorted(data)
    return [len(sorted_data[:i+1])/len(data) for i in range(len(data))]

def ProbabilityDensityFunction(data, bins=10):
    # 计算概率密度函数（Probability Density Function, PDF）
    histrogram, bin_edges = np.histogram(data, bins=bins, density=True)
    return histrogram

def rank_data(data):
    # 计算列表的排序索引
    sorted_data = sorted([(value, idx) for idx, value in enumerate(data)])
    return [idx for value, idx in sorted_data]

def count_inversions(data):
    # 计算列表的逆序对数量
    return sum(1 for i in range(len(data)) for j in range(i+1, len(data)) if data[i] > data[j])

def MAD(data):
    # 计算列表的中位数绝对偏差（MAD）
    median_val = np.median(data)
    return np.median(np.abs(data - median_val))

def M2(data):
    # 计算列表元素的二阶矩（M2）
    n = len(data)
    mean = np.mean(data)
    return sum((x - mean) ** 2 for x in data) / n

def entropy(data):
    # 计算信息熵
    unique_values = set(data)
    probabilities = [data.count(value) / len(data) for value in unique_values]
    return -sum(p * log2(p) for p in probabilities)

def auto_correlation(data, lag=1):
    # 计算列表的自动相关性
    series = pd.Series(data)
    return series.autocorr(lag)

def jackknife_statistics(data):
    # 计算Jackknife统计量
    return [variance_inflation_factor(pd.Series(data), i) for i in range(len(data))]

def frequency_count(data):
    freq_dict = {}
    # 计算列表的元素频率
    for item in data:
        if item in freq_dict:
            freq_dict[item] += 1
        else:
            freq_dict[item] = 1
    return freq_dict

def frequency_distribution(data, bins=10):
    # 生成数据的频率分布表
    histogram, bin_edges = np.histogram(data, bins=bins)
    return histogram, bin_edges

def mad_ratio(data):
    # 计算列表的中位数绝对偏差比率（Median Absolute Deviation Ratio）
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    return mad / np.std(data)

def linear_trend(data):
    # 检测列表中的线性趋势
    x = range(len(data))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, data)
    return slope, intercept, r_value

def trimmed_mean(data, proportion=0.1):
    # 计算列表的三角矩（Trimmed Mean）
    sorted_data = sorted(data)
    trim_amnt = int(len(data) * proportion)
    trimmed_data = sorted_data[trim_amnt:-trim_amnt]
    return np.mean(trimmed_data)

def calculate_T_statistic(sample, total):
    return (np.mean(sample) - np.mean(total)) / (np.std(sample) / sqrt(len(sample)))

def CoefficientOfVariation(data):
    return np.std(data)/np.mean(data)*100

def calculate_F_and_P_statistic(data1, data2):
    f_statistic, p_value = stats.f_oneway(data1, data2)
    return f_statistic, p_value

def calculate_F_statistic(data1, data2):
    return stats.f_oneway(data1, data2)[0]

def calculate_P_statistic(data1, data2):
    return stats.f_oneway(data1, data2)[1]

def Pearson_correlation_coefficient(data_x,data_y):
    return stats.pearsonr(data_x, data_y)

statistics_funcs = [mean, max, min, standard_deviation, mode, variance, median, range_ptp, percentile, skew, kurtosis, correlation, covariance,
                    moving_average, EWMA, z_scores, CumulativeDistributionFunction,
                    ProbabilityDensityFunction, MAD, M2, entropy, auto_correlation, jackknife_statistics, frequency_count, mad_ratio,
                    linear_trend, trimmed_mean, calculate_F_statistic, calculate_T_statistic, calculate_P_statistic, CoefficientOfVariation, Pearson_correlation_coefficient]
#extra :percentile(8)+percent ;correlation(11)- ;covariance(12)- ;moving_average(13)+window_size ;EWMA(14)+alpha ;calculate_F_statistic(27)- ;
# calculate_T_statistic(28)- ;calculate_P_statistic(29)- ;Pearson_correlation_coefficient(31)-



class Message_window:
    """
    a class that is used to show messages.
    #using tkinter and pygame(maybe)
    """


    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏tkinter窗口
        self.YES_NO = 0
        self.RETRY_CANCEL = 1
        self.OK_CANCEL = 2
        self.QUESTION = 3
        self.YES_NO_CANCEL = 4

    def warning(self, message='Warning', title='WARNING'):
        """
        :param title:
        :param message:
        """
        self.root.withdraw()  # 隐藏tkinter窗口
        messagebox.showwarning(title=title, message=message)

    def error(self, message, title='ERROR'):
        """
        :param title:
        :param message:
        """
        self.root.withdraw()  # 隐藏tkinter窗口
        messagebox.showerror(title=title, message=message)

    def browser(self, title="open a file", types=None, caption="C:\\"):
        """

        :param title:
        :param types:
        :param caption:
        """
        self.root.withdraw()  # 隐藏tkinter窗口
        if types is None:
            types = [('ALL', '*')]
        self.select_file(title, types, caption)

    def select_file(self, title="open a file", types=None, dir='C\\:'):
        """

        :param title:
        :param types:
        :param dir:
        """
        if types is None:
            types = [('all', '*')]

        self.root.withdraw()  # 隐藏tkinter窗口
        self.file_name = filedialog.askopenfilename(title=title, filetypes=types, initialdir=dir)  # 显示文件选择对话框

    def question(self, title='QUESTION', question='Question', Q_type=None):
        """

        :param title:
        :param question:
        :param Q_type:
        :return:
        """
        self.root.withdraw()  # 隐藏tkinter窗口
        if Q_type is None:
            Q_type = self.YES_NO
        if Q_type == self.YES_NO:
            answer = messagebox.askyesno(title, question)
        elif Q_type == self.OK_CANCEL:
            answer = messagebox.askokcancel(title, question)
        elif Q_type == self.RETRY_CANCEL:
            answer = messagebox.askretrycancel(title, question)
        elif Q_type == self.QUESTION:
            answer = messagebox.askquestion(title, question)
        elif Q_type == self.YES_NO_CANCEL:
            answer = messagebox.askyesnocancel(title, question)
        else:
            raise TypeError("No matching types!!!")
        return answer

    def get_file_name(self):
        """

        :return: str
        """
        try:
            return self.file_name
        except Exception:
            return None

    def message(self,message='Message',  title='MESSAGE'):
        """

        :param title:
        :param message:
        """
        self.root.withdraw()  # 隐藏tkinter窗口
        messagebox.showinfo(title, message)


message_window = Message_window()


def charting(charting_type, mul=False, fig=None, num=1, max=1, pie_pct='%1.2f%%', **all_values):
    """
    :param pie_pct:
    :param charting_type:
    :param fig:
    :param num:
    :param mul:
    :param all_values:
        pie:  <x,labels,colours=None>;
        hist: <x,density=False>;
        box:  <x -> 2d array,notch ->bool=False>;
        violin: <data -> array>;
        error bar: <x,y>;
        hist2d: <x,y,num=100>;
        hexbin: <x,y,num=100>;
        plot: <x,y>
        scatter: <x,y>
    """
    if mul:
        if len(sympy.divisors(max)) > 2:
            lcm = sympy.divisors(max)[-2]
        else:
            lcm = sympy.divisors(max)[0]
        x = max // lcm
        if x > max // x:
            y = max // x
        else:
            x = max // x
            y = max // x
        if charting_type not in ['hist', 'violin', 'hexbin', 'box', 'error bar', 'hist2d', 'pie', 'plot', 'scatter']:
            raise TypeError("'" + str(
                charting_type) + "' is not in available types :'hist','violin','hexbin','box','error bar','hist2d','pie','scatter'\n")
        plot = fig.add_subplot(x, y, num)
        if charting_type == 'pie':
            if len(all_values) == 2:
                plot.pie(all_values['x'], labels=all_values['labels'], autopct=(pie_pct))
            else:
                plot.pie(all_values['x'], labels=all_values['labels'], colors=all_values['colours'], autopct=pie_pct)
        elif charting_type == 'box':
            if len(all_values) == 1:
                plot.boxplot(all_values['x'])
            else:
                plot.boxplot(all_values['x'], notch=all_values['notch'])
        elif charting_type == 'hist':
            if len(all_values) == 1:
                plot.hist(all_values['x'])
            else:
                plot.hist(all_values['x'], density=all_values['density'])
        elif charting_type == 'violin':
            plot.violinplot(all_values['data'])
        elif charting_type == 'error bar':
            plot.errorbar(all_values['x'], all_values['y'])
        elif charting_type == 'hist2d':
            if len(all_values) == 2:
                plot.hist2d(all_values['x'], all_values['y'], 100, cmap='Blues')
            else:
                plot.hist2d(all_values['x'], all_values['y'], all_values['number'], cmap='Blues')
        elif charting_type == 'hexbin':
            if len(all_values) == 2:
                plot.hexbin(all_values['x'], all_values['y'], cmap='Blues')
            else:
                plot.hexbin(all_values['x'], all_values['y'], cmap='Blues', gridsize=all_values['number'])
        elif charting_type == "plot":
            plot.plot(all_values['x'], all_values['y'])
        elif charting_type == 'scatter':
            plot.scatter(all_values['x'], all_values['y'])
    else:
        if charting_type not in ['hist', 'violin', 'hexbin', 'box', 'error bar', 'hist2d', 'pie', 'plot', 'scatter']:
            raise TypeError("'" + str(
                charting_type) + "' is not in available types :'hist','violin','hexbin','box','error bar','hist2d','pie','plot','scatter'\n")
        if charting_type == 'pie':
            if len(all_values) == 2:
                plt.pie(all_values['x'], labels=all_values['labels'], autopct=pie_pct)
                plt.show()
            else:
                plt.pie(all_values['x'], labels=all_values['labels'], colors=all_values['colours'], autopct=pie_pct)
                plt.show()
        elif charting_type == 'box':
            if len(all_values) == 1:
                plt.boxplot(all_values['x'])
                plt.show()
            else:
                plt.boxplot(all_values['x'], notch=all_values['notch'])
                plt.show()
        elif charting_type == 'hist':
            if len(all_values) == 1:
                plt.hist(all_values['x'])
                plt.show()
            else:
                plt.hist(all_values['x'], density=all_values['density'])
                plt.show()
        elif charting_type == 'violin':
            plt.violinplot(all_values['data'])
            plt.show()
        elif charting_type == 'error bar':
            plt.errorbar(all_values['x'], all_values['y'])
            plt.show()
        elif charting_type == 'hist2d':
            if len(all_values) == 2:
                plt.hist2d(all_values['x'], all_values['y'], 100, cmap='Blues')
            else:
                plt.hist2d(all_values['x'], all_values['y'], all_values['number'], cmap='Blues')
            plt.show()
        elif charting_type == 'hexbin':
            if len(all_values) == 2:
                plt.hexbin(all_values['x'], all_values['y'], cmap='Blues')
                plt.show()
            else:
                plt.hexbin(all_values['x'], all_values['y'], cmap='Blues', gridsize=all_values['number'])
                plt.show()
        elif charting_type == "plot":
            plt.plot(all_values['x'], all_values['y'])
            plt.show()
        elif charting_type == 'scatter':
            plt.scatter(all_values['x'], all_values['y'])
            plt.show()


def charts(window, clock, choices, **all_values):
    """

    :param window:
    :param clock:
    :param choices:
    :param all_values:
    """
    fig = plt.figure()
    try:
        xs = all_values['xs']
        ys = all_values['ys']
        one_table = all_values['one_table']
        mult = True
    except KeyError:
        mult = False
    if type(choices) != str and (type(choices) == list or type(choices) == tuple):
        if len(choices) > 0:
            m = choices
            max_num = len(m)
            if not mult:
                for i, j in zip(m, range(len(m))):
                    if i == 0:
                        charting('pie', True, fig, j + 1, max_num, x=all_values['x'], labels=all_values['labels'])
                    elif i == 1:
                        charting('hist', True, fig, j + 1, max_num, x=all_values['x'])
                    elif i == 2:
                        charting('box', True, fig, j + 1, max_num, x=all_values['x'])
                    elif i == 3:
                        charting('violin', True, fig, j + 1, max_num, data=all_values['x'])
                    elif i == 4:
                        charting('error bar', True, fig, j + 1, max_num, x=all_values['x'], y=all_values['y'])
                    elif i == 5:
                        label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                            'input the number of hist of the each sides', 'OK',
                                                            'CANCEL', backgroundColor=(90, 90, 150),
                                                            promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        charting('hist2d', True, fig, j + 1, max_num, x=all_values['x'], y=all_values['y'],
                                 number=int(label))
                    elif i == 6:
                        label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                            'input the number of hex of the each sides', 'OK', 'CANCEL',
                                                            backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                            inputTextColor=(0, 0, 0))
                        charting('hexbin', True, fig, j + 1, max_num, x=all_values['x'], y=all_values['y'],
                                 number=int(label))
                    elif i == 7:
                        charting('plot', True, fig, j + 1, max_num, x=all_values['x'], y=all_values['y'])

            else:
                x_index = y_index = 0
                for i, j in zip(m, range(len(m))):
                    if i == 0:
                        x = xs[x_index]
                        curr_label = all_values['labels'][j]
                        if one_table:
                            charting('pie', True, fig, j + 1, max_num, x=x, labels=curr_label)
                        else:
                            plt.pie(x, labels=curr_label)
                        x_index += 1
                    elif i == 1:
                        x = xs[x_index]
                        if one_table:
                            charting('hist', True, fig, j + 1, max_num, x=x)
                        else:
                            plt.hist(x)
                        x_index += 1
                    elif i == 2:
                        x = xs[x_index]
                        if one_table:
                            charting('box', True, fig, j + 1, max_num, x=x)
                        else:
                            plt.boxplot(x)
                        x_index += 1
                    elif i == 3:
                        x = xs[x_index]
                        if one_table:
                            charting('violin', True, fig, j + 1, max_num, data=x)
                        else:
                            plt.violinplot(x)
                        x_index += 1
                    elif i == 4:
                        x = xs[x_index]
                        y = ys[y_index]
                        if one_table:
                            charting('error bar', True, fig, j + 1, max_num, x=x, y=y)
                        else:
                            plt.errorbar(x, y)
                        x_index += 1
                        y_index += 1
                    elif i == 5:
                        x = xs[x_index]
                        y = ys[y_index]
                        number = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                             'input the number of hist of the each sides', 'OK',
                                                             'CANCEL', backgroundColor=(90, 90, 150),
                                                             promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        if one_table:
                            charting('hist2d', True, fig, j + 1, max_num, x=x, y=y,
                                     number=int(number))
                        else:
                            plt.hist2d(x, y, int(number))
                        x_index += 1
                        y_index += 1
                    elif i == 6:
                        x = xs[x_index]
                        y = ys[y_index]
                        number = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                             'input the number of hex of the each sides', 'OK',
                                                             'CANCEL', backgroundColor=(90, 90, 150),
                                                             promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        if one_table:
                            charting('hexbin', True, fig, j + 1, max_num, x=x, y=y, number=int(number))
                        else:
                            plt.hexbin(x, y, gridsize=int(number), cmap='Blues')
                        x_index += 1
                        y_index += 1
                    elif i == 7:
                        x = xs[x_index]
                        y = ys[y_index]
                        if one_table:
                            charting('plot', True, fig, j + 1, max_num, x=x, y=y)
                        else:
                            plt.plot(x, y)
                        x_index += 1
                        y_index += 1
                    elif i == 8:
                        x = xs[x_index]
                        y = ys[y_index]
                        if one_table:
                            charting('scatter', True, fig, j + 1, max_num, x=x, y=y)
                        else:
                            plt.scatter(x, y)
                        x_index += 1
                        y_index += 1

            plt.show()
        else:
            if choices[0] == 0:
                charting('pie', x=all_values['x'], labels=all_values['labels'])
            elif choices[0] == 1:
                charting('hist', x=all_values['x'])
            elif choices[0] == 2:
                charting('box', x=all_values['x'])
            elif choices[0] == 3:
                charting('violin', data=all_values['x'])
            elif choices[0] == 4:
                charting('error bar', x=all_values['x'], y=all_values['y'])
            elif choices[0] == 5:
                label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                    'input the number of hex of the each sides', 'OK', 'CANCEL',
                                                    backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                    inputTextColor=(0, 0, 0))
                try:
                    charting('hist2d', x=all_values['x'], y=all_values['y'], number=int(label))
                except:
                    charting('hist2d', x=all_values['x'], y=all_values['y'], number=30)
            elif choices[0] == 6:
                label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                    'input the number of hex of the each sides', 'OK', 'CANCEL',
                                                    backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                    inputTextColor=(0, 0, 0))
                charting('hexbin', x=all_values['x'], y=all_values['y'], number=int(label))
            elif choices[0] == 7:
                charting('hexbin', x=all_values['x'], y=all_values['y'])
            elif choices[0] == 8:
                charting('scatter', x=all_values['x'], y=all_values['y'])
    elif type(choices) == int:
        if choices == 0:
            charting('pie', x=all_values['x'], labels=all_values['labels'])
        elif choices == 1:
            charting('hist', x=all_values['x'])
        elif choices == 2:
            charting('box', x=all_values['x'])
        elif choices == 3:
            charting('violin', data=all_values['x'])
        elif choices == 4:
            charting('error bar', x=all_values['x'], y=all_values['y'])
        elif choices == 5:
            label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                'input the number of hex of the each sides', 'OK', 'CANCEL',
                                                backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                inputTextColor=(0, 0, 0))
            charting('hist2d', x=all_values['x'], y=all_values['y'], number=int(label))
        elif choices == 6:
            label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                'input the number of hex of the each sides', 'OK', 'CANCEL',
                                                backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                inputTextColor=(0, 0, 0))
            charting('hexbin', x=all_values['x'], y=all_values['y'], number=int(label))
        elif choices == 7:
            charting('plot', x=all_values['x'], y=all_values['y'])
        elif choices == 8:
            charting('scatter', x=all_values['x'], y=all_values['y'])


def load_label(window, num):
    """

    :param window:
    :param num:
    :return:
    """
    global message_window
    message_window.browser("Choose an Excel file for the label's source", [('EXCEL files', '.xlsx')])
    file_name = message_window.file_name
    if file_name == '':
        message_window.error("failed to process because of empty file name")
        return
    choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect label',
                                        "by line(----)", 'by column(| | |)')
    file = ExcelMgr(file_name)
    file_data = file.data
    if not choice:
        col = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'input column number(starts with 0)', 'OK',
                                          'CANCEL',
                                          backgroundColor=(90, 90, 150),
                                          promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        try:
            col_num = int(col)
        except TypeError:
            if col is not None:
                message_window.error('bad inputs for int ' + str(col))
            return
        cols_start = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                 'input cols start position of arrange (starts with 0)', 'OK',
                                                 'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                 inputTextColor=(0, 0, 0))
        try:
            col_start_num = int(cols_start)
        except TypeError:
            if cols_start is not None:
                message_window.error('bad inputs for int ' + str(cols_start))
            return
        cols_end = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                               'input cols end position of arrange(include)', 'OK', 'CANCEL',
                                               backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                               inputTextColor=(0, 0, 0))
        try:
            col_end_num = int(cols_end)
        except TypeError:
            if cols_end is not None:
                message_window.error('bad inputs for int ' + str(cols_end))
            return
        try:
            data = file_data
            data = [line_[col_num] for line_ in data]
            data = data[col_start_num:col_end_num + 1]
            if len(data) > num:
                message_window.warning("too many labels!!! we will cut to the right number")
                labels = data[0:num]
            elif len(data) == 0:
                message_window.error("no labels has chosen")
                return
            elif len(data) < num:
                message_window.error("too less labels!! function ends")
                return
            else:
                labels = data
            return labels
        except Exception as e:
            message_window.error(str(e))
            return
    else:
        line = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'input line number(starts with 0)', 'OK',
                                           'CANCEL',
                                           backgroundColor=(90, 90, 150),
                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        try:
            line_num = int(line)
        except TypeError:
            if line is not None:
                message_window.error('bad inputs for int ' + str(line))
            return
        line_start = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                 'input arrange start position of line (starts with 0)' + str(
                                                     line_num), 'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                 promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        try:
            line_start_num = int(line_start)
        except TypeError:
            if line_start is not None:
                message_window.error('bad inputs for int ' + str(line_start))
            return
        line_end = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                               'input end position of line ' + str(line_num),
                                               'OK', 'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                               inputTextColor=(0, 0, 0))
        try:
            line_end_num = int(line_end)
        except TypeError:
            if line_end is not None:
                message_window.error('bad inputs for int ' + str(line_end))
            return
        try:
            num = 0
            data = file_data[line_num]
            data = data[line_start_num:line_end_num + 1]
        except IndexError as e:
            message_window.error(str(e))
            return
        if len(data) > num:
            message_window.warning("too many labels!!! we will cut to the right number")
            labels = data[0:num]
        elif len(data) < num:
            message_window.error("too less labels!! function ends")
            return
        elif len(data) == 0:
            message_window.error("no labels has chosen")
            return
        else:
            labels = data
        return labels


def data_visualize_2d(window, clock, debug=False):
    """
    version:3.1
    develop time:2025-1-17
    """
    global message_window
    plt.close('all')
    fig = plt.figure()
    fig.clear()
    data_collecting_method = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect data',
                                        '.xlsx file', "by inputting the data manually")
    mult = pyghelpers.textYesNoDialog(window, (0, 300, 600, 300), 'you want to draw chart(s) on',
                                      'multiple separate chart tables', "one signal chart table")
    many_charts = pyghelpers.textYesNoDialog(window, (0, 300, 600, 300), 'How many charts of each type do you want to draw',
                                      'many', "only one each type")
    pie = False
    if mult:
        diff_source = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                 'you want to select the data for charts from',
                                                 'multiple .xlsx files', "one signal .xlsx file")

    if data_collecting_method:  #################################################  load from excel files ###########################################################################

        message_window.browser("Choose an Excel file for the data's source", [('EXCEL files', '.xlsx')])
        file_name = message_window.file_name
        if file_name == '':
            message_window.error("failed to process because of empty file name")
            return
        try:
            file = ExcelMgr(file_name)
            file_data = file.data
            charting_type_selector = CheckBox(9, ['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'], 9,
                         window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30, buttons_adjust_length=0, background_color=(90, 90, 150))
            list_preview = WindowListViewer(file_data, (1004, 410), window, (0, 200))
            if type(charting_type_selector.clicked_choices) == str:
                return
            elif len(charting_type_selector.clicked_choices) == 0:
                choice_ = message_window.question("you didn't choice any type of charts, do you want to exit?")
                if not choice_:
                    return data_visualize_2d(window, clock)
                else:
                    return
            if mult:
                diff_file_source = diff_source
            else:
                diff_file_source = False
            by_line = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect data',
                                                "by line(----)", 'by column(| | |)')
            if not mult:
                xs = ys = []
                pie = False
            pie_labels = []
            pie_value_poses = []
            chart_choices = []
            if many_charts:
                for charting_type_selector in charting_type_selector.clicked_choices:
                    num = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'How many '+['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'][charting_type_selector]+' charts do you want to draw?',
                                                                      'OK',
                                                                      'CANCEL', backgroundColor=(90, 90, 150),
                                                                      promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                    try:
                        num = int(num)
                    except Exception:
                        message_window.error("Can't turn "+str(num)+' into an integer')
                        return
                    if num < 0:
                        message_window.error("You can't draw negative charts!")
                        return
                    else:
                        for i in range(num):
                            chart_choices.append(charting_type_selector)
            else:
                chart_choices = charting_type_selector.clicked_choices
            for charting_type_selector, j in zip(chart_choices, range(len(chart_choices))):
                if type(charting_type_selector) is str:
                    break
                if j >= 1 and diff_file_source:
                    message_window.browser("Choose an Excel file for the data's source for " +
                                           ['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot',
                                            'scatter'][charting_type_selector], [('EXCEL files', '.xlsx')])
                    file_name = message_window.file_name
                    if file_name is None:
                        message_window.error("failed to process because of empty file name")
                        return
                    file = ExcelMgr(file_name)
                    file_data = file.data
                    list_preview = WindowListViewer(file_data, (1004, 410), window, (0, 200))
                if not by_line:####by column
                    if charting_type_selector <= 3:
                        arrange_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input arrange number',
                                                              [list_preview.draw],[list_preview.handle_event],'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if arrange_num is None:
                            message_window.error('no inputs is given')
                            return
                        col_start_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                 'input cols start position of arrange (starts with 0)' + str(
                                                                     arrange_num), [list_preview.draw],[list_preview.handle_event],'OK',
                                                                 'CANCEL', backgroundColor=(90, 90, 150),
                                                                 promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if col_start_num is None:
                            message_window.error('no inputs is given');return
                        col_end_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                               'input cols end position of arrange (include)' + str(
                                                                   arrange_num),
                                                               [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if col_end_num is None:
                            message_window.error('no inputs is given')
                            return
                        try:
                            data = []
                            num = 0
                            avail_num = 0
                            for i in file_data[col_start_num - 1:col_end_num]:
                                if type(i[arrange_num - 1]) not in [int, float]:
                                    pass
                                else:
                                    avail_num += 1
                                    data.append(i[arrange_num - 1])
                                num += 1
                            if avail_num != num:
                                message_window.warning('we found ' + str(
                                    num - avail_num) + ' valid data(s) in your file,we will ignore them(it)')
                            if len(data) == 0:
                                message_window.error('Exit because of no available data')
                                return
                        except IndexError as e:
                            message_window.error(str(e))
                            return
                        if charting_type_selector == 0:  # pie chart needs user to input labels
                            if mult:
                                pie = True
                            label_choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                      'please input the labels ',
                                                                      "manually", 'automatically create')
                            if label_choice:
                                label = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                    "input you labels split each other with ';'"+'(number:' + str(
                                                                        len(data)) + '),input none to set labels automatically',
                                                                    [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                                if label is not None:
                                    label = label.split(";")
                                    if len(label) > len(data):
                                        message_window.warning(
                                            "label's num (" + str(len(label)) + ", is higher than data's num (" + str(
                                                len(data))
                                            + ",system will adjust this by adding labels automatically")
                                        label = label[:len(data)]
                                    elif len(label) < len(data):
                                        message_window.warning(
                                            "label's num (" + str(len(label)) + ", is lower than data's num (" + str(
                                                len(data)) + ',system will adjust this by adding labels automatically')
                                        k = len(label)
                                        label = label + ['label ' + str(k + a) for a in range(len(data) - len(label))]

                                else:
                                    label = ["label " + str(b + 1) for b in range(len(data))]
                                if mult:
                                    charts(window, clock, charting_type_selector, x=data, labels=label)
                                else:
                                    pie_data_index = len(xs)
                                    xs.append(data)
                                    pie_label = label
                                    pie_labels.append(pie_label)
                                    pie_value_poses.append(pie_data_index)
                            else:
                                label_source = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                          "please select the labels' source",
                                                                          "Excel files(*.xlsx)", 'automatically create')
                                if label_source:
                                    label = load_label(window, len(data))
                                    if label is None:
                                        message_window.error("FATAL ERROR:failed to load labels;function ends")
                                        return
                                else:
                                    label = ["label " + str(b + 1) for b in range(len(data))]
                                    if mult:
                                        charts(window, clock, charting_type_selector, x=data, labels=label)
                                    else:
                                        pie_data_index = len(xs)
                                        xs.append(data)
                                        pie_value_poses.append(pie_data_index)
                                        pie_label = label
                                        pie_labels.append(pie_label)

                        else:
                            if mult:
                                charts(window, clock, charting_type_selector, x=data)
                            else:
                                xs.append(data)
                    else:  # types likes hexbin,hist2d and error bar ||#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
                        arrange_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                              'input arrange number', [list_preview.draw],[list_preview.handle_event],'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if arrange_num is None:
                            message_window.error('no inputs is given')
                            return
                        col_start_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                 'input cols start position of arrange (start with 0)' + str(
                                                                     arrange_num), [list_preview.draw],[list_preview.handle_event],'OK',
                                                                 'CANCEL', backgroundColor=(90, 90, 150),
                                                                 promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if col_start_num is None:
                            message_window.error('no inputs is given')
                            return
                        col_end_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                               'input cols end position of arrange (include)' + str(
                                                                   arrange_num), [list_preview.draw],[list_preview.handle_event],'OK',
                                                               'CANCEL', backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if col_end_num is None:
                            message_window.error('no inputs is given')
                            return
                        try:
                            data = []
                            num = 0
                            avail_num = 0
                            for i in file_data[col_start_num - 1:col_end_num]:
                                if type(i[arrange_num - 1]) not in [int, float]:
                                    pass
                                else:
                                    avail_num += 1
                                    data.append(i[arrange_num - 1])
                                num += 1
                            if avail_num != num:
                                message_window.warning('we found ' + str(
                                    num - avail_num) + ' valid data in your file,we will ignore them')
                        except IndexError as e:
                            message_window.error(str(e))
                            return
                        if charting_type_selector == 4:  # error bar
                            if mult:
                                charts(window, clock, charting_type_selector, x=data)
                            else:
                                xs.append(data)
                        elif charting_type_selector == 5 or charting_type_selector == 6 or charting_type_selector == 7 or charting_type_selector == 8:
                            #  input the 'y' agreement
                            arrange_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input arrange number',
                                                                  [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                            if arrange_num is None:
                                message_window.error('no inputs is given')
                                return
                            col_start_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                     'input cols start position of arrange (starts with 0)' + str(
                                                                         arrange_num), [list_preview.draw],[list_preview.handle_event],'OK',
                                                                     'CANCEL', backgroundColor=(90, 90, 150),
                                                                     promptTextColor=(0, 0, 0),
                                                                     inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                            if col_start_num is None:
                                message_window.error('no inputs is given')
                                return
                            col_end_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                   'input cols end position of arrange (include)' + str(
                                                                       arrange_num),
                                                                   [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                            if col_end_num is None:
                                message_window.error('no inputs is given')
                                return
                            try:
                                data_y = []
                                num = 0
                                avail_num = 0
                                for i in file_data[col_start_num - 1:col_end_num]:
                                    if type(i[arrange_num - 1]) not in [int, float]:
                                        pass
                                    else:
                                        avail_num += 1
                                        data_y.append(i[arrange_num - 1])
                                    num += 1
                                if avail_num != num:
                                    message_window.warning('we found ' + str(
                                        num - avail_num) + ' valid data in your file,we will ignore them')
                            except IndexError as e:
                                message_window.error(str(e))
                                return
                            if mult:
                                charts(window, clock, charting_type_selector, x=data, y=data_y)
                            else:
                                xs.append(data)
                                ys.append(data_y)

                    #                                       by column (| | |)[end]
######################-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
                else:  # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
######################-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
                    #                                       by line (---)[start]
                    if charting_type_selector <= 3:
                        line_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input line number', [list_preview.draw]
                                                                ,[list_preview.handle_event],'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if line_num is None:
                            message_window.error('no inputs is given')
                            return
                        line_start_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                 'input arrange start position("0"means arrange 1) of line ' + str(
                                                                     line_num), [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL',
                                                                 backgroundColor=(90, 90, 150),allow_float=False, allow_negative=False,
                                                                 promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))

                        if line_start_num is None:
                            message_window.error('no inputs is given')
                            return
                        line_end_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                               'input arrange end position of line ' + str(line_num),
                                                               [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if line_end_num is None:
                            message_window.error('no inputs is given')
                            return
                        try:
                            data = []
                            num = 0
                            avail_num = 0
                            load_data = file_data[line_num][line_start_num:line_end_num + 1]
                            for i in load_data:
                                if type(i) in [int, float]:
                                    avail_num += 1
                                    data.append(i)
                                else:
                                    pass
                                num += 1
                            if avail_num != num:
                                message_window.warning('we found ' + str(
                                    num - avail_num) + ' valid data in your file,we will ignore them')
                            if len(data) == 0:
                                return
                        except IndexError as e:
                            message_window.error(str(e))
                            return
                        if charting_type_selector == 0:  # pie chart needs user to input labels
                            label_choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                      'please input the labels ', "manually",
                                                                      'automatically create')
                            pie = True
                            if label_choice:
                                label = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                    "input you labels split each other with ';',(number:" + str(
                                                                        len(data)) + '),input none to set labels automatically',
                                                                    [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                                if label is not None:
                                    label = label.split(";")
                                    if len(label) > len(data):
                                        message_window.warning(
                                            "label's num (" + str(len(label)) + ", is higher than data's num (" + str(
                                                len(data)) + ",system will adjust this by canceling labels automatically")
                                        label = label[:len(data)]
                                    elif len(label) < len(data):
                                        message_window.warning(
                                            "label's num (" + str(len(label)) + ", is lower than data's num (" + str(
                                                len(data)) + ',system will adjust this by adding labels automatically')
                                        k = len(label)
                                        label = label + ['label ' + str(k + a) for a in range(len(data) - len(label))]

                                else:
                                    label = ["label " + str(b + 1) for b in range(len(data))]
                                if mult:
                                    charts(window, clock, charting_type_selector, x=data, labels=label)
                                else:
                                    pie_value_poses.append(len(xs))
                                    xs.append(data)
                                    pie_label = label
                                    pie_labels.append(pie_label)
                            else:
                                label_source = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                          "please select the labels' source",
                                                                          "Excel files(*.xlsx)",
                                                                          'automatically create')
                                if label_source:
                                    label = load_label(window, len(data))
                                    if label is None:
                                        message_window.error("FATAL ERROR:failed to load labels;function ends")
                                        return
                                else:
                                    label = ["label " + str(b + 1) for b in range(len(data))]
                                    if mult:
                                        charts(window, clock, charting_type_selector, x=data, labels=label)
                                    else:
                                        pie_value_poses.append(len(xs))
                                        xs.append(data)
                                pie_label = label
                                pie_labels.append(pie_label)
                        else:
                            if mult:
                                charts(window, clock, charting_type_selector, x=data)
                            else:
                                xs.append(data)
                    else:
                        line_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                           'input line number', [list_preview.draw],[list_preview.handle_event],'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if line_num is None:
                            message_window.error('no inputs is given')
                            return
                        line_start_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                 'input arrange start position of line ' + str(
                                                                     line_num), [list_preview.draw],[list_preview.handle_event],'OK',
                                                                 'CANCEL', backgroundColor=(90, 90, 150),
                                                                 promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if line_start_num is None:
                            message_window.error('no inputs is given')
                            return
                        line_end_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                               'input arrange end position of line ' + str(line_num),
                                                               [list_preview.draw],[list_preview.handle_event],'OK',
                                                               'CANCEL', backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if line_end_num is None:
                            message_window.error('no inputs is given')
                            return
                        try:
                            data = []
                            num = 0
                            avail_num = 0
                            load_data = file_data[line_num][line_start_num:line_end_num + 1]
                            for i in load_data:
                                if type(i) in [int, float]:
                                    avail_num += 1
                                    data.append(i)
                                else:
                                    pass
                                num += 1
                            if avail_num != num:
                                message_window.warning('we found ' + str(
                                    num - avail_num) + ' valid data in your file,we will ignore them')
                        except IndexError as e:
                            message_window.error(str(e))
                            return
                        if charting_type_selector == 4:
                            if mult:
                                charts(window, clock, charting_type_selector, x=data)
                            else:
                                xs.append(data)
                        elif charting_type_selector == 5 or charting_type_selector == 6 or charting_type_selector == 7 or charting_type_selector == 8:
                            line_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input line number for y',
                                                               [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                            if line_num is None:
                                message_window.error('no inputs is given')
                                return
                            line_start_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                     'input arrange start position of line ' + str(line_num), [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL',
                                                                     backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                            if line_start_num is None:
                                message_window.error('no inputs is given')
                                return
                            line_end_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                   'input arrange end position of line ' + str(
                                                                       line_num), [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL',
                                                                   backgroundColor=(90, 90, 150), allow_float=False, allow_negative=False,
                                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))

                            if line_end_num is None:
                                message_window.error('no inputs is given')
                                return
                            try:
                                num = 0
                                avail_num = 0
                                data_y = file_data[line_num]
                                data_y = data_y[line_start_num:line_end_num + 1]
                                for i in data_y:
                                    if type(i) not in [int, float]:
                                        pass
                                    else:
                                        avail_num += 1
                                    num += 1
                                if avail_num != num and avail_num > 0:
                                    message_window.warning('we found ' + str(
                                        num - avail_num) + ' valid data in your file,we will ignore them')
                                elif avail_num == 0:
                                    message_window.error(
                                        "this program will exit because of no available value can be used to chart")
                                    return
                            except IndexError as e:
                                message_window.error(str(e))
                                return
                            if mult:
                                charts(window, clock, charting_type_selector, x=data, y=data_y)
                            else:
                                xs.append(data)
                                ys.append(data_y)

            if mult:# multiple separate charting windows
                if not pie:
                    charts(window, clock, chart_choices, xs=xs, ys=ys, one_table=False)
                else:
                    charts(window, clock, chart_choices, xs=xs, ys=ys, labels=pie_labels, one_table=False)

            else:# all be drawn in one window
                if not pie:
                    charts(window, clock, chart_choices, xs=xs, ys=ys, one_table=True)
                else:
                    charts(window, clock, chart_choices, xs=xs, ys=ys, labels=pie_labels, one_table=True)

            return
        except Exception as e:
            error_log = open("error_log.txt", "w")
            error_log.write("An error occurred: {}\n".format(e))
            traceback.print_exc(file=error_log)
            error_log.write("\n")
            error_log.close()
            message_window.error("An error occurred. Please check the error log for details.")
            if debug:
                raise e
            return

    else:##################################################### input manually ###############################################################################

        if mult:
            xs = ys = []
            pie = False
            pie_label = ''
        data = pyghelpers.textAnswerDialog(window, (200, 100, 500, 200),
                                           "input you data split each other with ';',(if the data isn't in a tuple or list)",
                                           'OK', 'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                           inputTextColor=(0, 0, 0))
        try:
            data = data.split(";")
            data2 = []
            for i in data:
                if ('(' in i and ")" in i) or ('[' in i and "]" in i):
                    data2.append(eval(i))
                else:
                    data2.append(float(i))
            data = data2
            charting_type_selector = CheckBox(9, ['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'], 9,
                         window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30, buttons_adjust_length=100,background_color=(90, 90, 150))
            choices = charting_type_selector.clicked_choices
            pie_labels = []
            pie_value_poses = []
            chart_choices = []
            for charting_type_selector in charting_type_selector.clicked_choices:
                num = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'How many ' +
                                                  ['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin',
                                                   'plot', 'scatter'][charting_type_selector] + ' charts do you want to draw?',
                                                  'OK',
                                                  'CANCEL', backgroundColor=(90, 90, 150),
                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                try:
                    num = int(num)
                except Exception:
                    message_window.error("Can't turn " + str(num) + ' into an integer')
                    return
                if num < 0:
                    message_window.error("You can't draw negative charts!")
                    return
                else:
                    for i in range(num):
                        chart_choices.append(charting_type_selector)
            for charting_type_selector in chart_choices:
                if type(charting_type_selector) is str:
                    break
                if charting_type_selector <= 4:
                    if charting_type_selector == 0:
                        label_choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                  'please input the labels ', "manually",
                                                                  'automatically create')
                        if label_choice:
                            label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                                "input you labels split each other with ';',(number:" + str(
                                                                    len(data)) + '),input none to set labels automatically',
                                                                'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                            if label is not None:
                                label = label.split(";")
                                if len(label) > len(data):
                                    message_window.warning(
                                        "label's num (" + str(len(label)) + ", is higher than data's num (" + str(
                                            len(data))
                                        + ",system will adjust this by canceling labels automatically")
                                    label = label[:len(data)]
                                elif len(label) < len(data):
                                    message_window.warning(
                                        "label's num (" + str(len(label)) + ", is lower than data's num (" + str(
                                            len(data)) + ',system will adjust this by adding labels automatically')
                                    k = len(label)
                                    label = label + ['label ' + str(k + a) for a in range(len(data) - len(label))]

                            else:
                                label = ["label " + str(b + 1) for b in range(len(data))]
                            if mult:
                                charts(window, clock, charting_type_selector, x=data, labels=label)
                            else:
                                pie = True
                                pie_label = label
                                pie_value_poses.append(len(xs))
                                xs.append(data)
                                pie_labels.append(pie_label)
                        else:
                            label_source = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                      "please select the labels' source",
                                                                      "Excel files(*.xlsx)", 'automatically create')
                            if label_source:
                                label = load_label(window, len(data))
                                if label is None:
                                    message_window.error("FATAL ERROR:failed to load labels;function ends")
                                    return
                            else:
                                label = ["label " + str(b + 1) for b in range(len(data))]
                                if mult:
                                    charts(window, clock, charting_type_selector, x=data, labels=label)
                                else:
                                    xs.append(data)
                            pie_label = label
                            pie_value_poses.append(len(xs))
                            xs.append(data)
                            pie_labels.append(pie_label)
                    else:
                        if mult:
                            charts(window, clock, charting_type_selector, x=data)
                        else:
                            xs.append(data)
                else:
                    data2 = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                        "input you NEXT group of data ,split each other with ' ',(if the data isn't in a tuple or list)",
                                                        'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                        promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                    data2 = data2.split(" ")
                    if not mult:
                        charts(window, clock, charting_type_selector, x=data, y=data2)
                    else:
                        xs.append(data)
                        ys.append(data2)
            if mult:
                if not pie:
                    charts(window, clock, chart_choices, xs=xs, ys=ys)
                else:
                    charts(window, clock, chart_choices, xs=xs, ys=ys, labels=pie_label)
            return
        except TypeError:
            message_window.error("bad inputs for float!")
            return
        except Exception as e:
            error_log = open("error_log.txt", "w")
            error_log.write("An error occurred: {}\n".format(e))
            error_log.write("Traceback:\n")
            traceback.print_exc(file=error_log)
            error_log.write("\n")
            error_log.close()
            message_window.error("An error occurred. Please check the error log for details.")
            if debug:
                raise e
            return


def loading_data(data_collecting_method, window, comments:str='', reload_data=True, file_data=None):
    global message_window
    if data_collecting_method:#from excel files
        if reload_data or file_data is None:
            message_window.browser("Choose an Excel file for the data's source", [('EXCEL files', '.xlsx')])
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
        choice = pyghelpers.textYesNoDialog(window, (0, 300, 600, 300), 'how do you want to collect data'+comments,
                                            "by line(----)", 'by column(| | |)')


        if not choice:  ####by column ################################################################################

            arrange_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input arrange number',
                                                           [list_preview.draw], [list_preview.handle_event], 'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

            if arrange_num is None:
                message_window.error('no inputs is given')
                return
            col_start_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                              'input cols start position of arrange (starts with 0)' + str(
                                                                  arrange_num), [list_preview.draw],
                                                              [list_preview.handle_event], 'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

            if col_start_num is None:
                message_window.error('no inputs is given')
                return
            col_end_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),'input cols end position of arrange (include)' + str(arrange_num),
                                                            [list_preview.draw], [list_preview.handle_event], 'OK',
                                                            'CANCEL', backgroundColor=(90, 90, 150),
                                                            promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

            if col_end_num is None:
                message_window.error('no inputs is given')
                return
            try:
                data = []
                num = 0
                avail_num = 0
                for i in file_data[col_start_num - 1:col_end_num]:
                    if type(i[arrange_num - 1]) in [int, float]:
                        avail_num += 1
                        data.append(i[arrange_num - 1])
                    num += 1
                if avail_num != num:
                    message_window.warning('we found ' + str(
                        num - avail_num) + ' valid data(s) in your file,we will ignore them(it)')
                if len(data) == 0:
                    message_window.error('Exit because of no available data')
                    return
            except IndexError as e:
                message_window.error(str(e))
                return

        else: ##### by line ################################################################################

            line_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input line number', [list_preview.draw]
                                                    , [list_preview.handle_event], 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

            if line_num is None:
                message_window.error('no inputs is given')
                return
            line_start_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                          'input arrange start position("0"means arrange 1) of line ' + str(
                                                              line_num), [list_preview.draw],
                                                          [list_preview.handle_event], 'OK', 'CANCEL',
                                                          backgroundColor=(90, 90, 150), allow_float=False, allow_negative=False,
                                                          promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))

            if line_start_num is None:
                message_window.error('no inputs is given')
                return
            line_end_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input arrange end position of line ' + str(line_num),
                                                        [list_preview.draw], [list_preview.handle_event], 'OK',
                                                        'CANCEL', backgroundColor=(90, 90, 150),
                                                        promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

            if line_end_num is None:
                message_window.error('no inputs is given')
                return
            try:
                num = 0
                avail_num = 0
                file_data = file_data[line_num][line_start_num:line_end_num + 1]
                data = []
                for i in file_data:
                    if type(i) in [int, float]:
                        data.append(i)
                        avail_num += 1
                    num += 1
                if avail_num != num:
                    message_window.warning('we found ' + str(
                        num - avail_num) + ' valid data in your file,we will ignore them')
                if len(data) == 0:
                    return
            except IndexError as e:
                message_window.error(str(e))
                return
    else:
        data = pyghelpers.textAnswerDialog(window, (200, 100, 500, 200),
                                           "input you data split each other with ';'",
                                           'OK', 'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                           inputTextColor=(0, 0, 0))
        data = data.split(";")
        data2 = []
        unavailable = 0
        for i in data:
            try:
                data2.append(float(i))
            except Exception:
                unavailable += 1
        if unavailable != 0:
            message_window.warning("there's "+str(unavailable)+' unavailable data in your inputs, they will be ignored.')
        data = data2
        list_preview = WindowListViewer([data], (1004, 410), window, (0, 200))

    if len(data) == 0:
        message_window.error('There is no available data, program exits.')
        return
    return data


def data_analyze(window, clock):
    plt.close('all')
    fig = plt.figure()
    fig.clear()
    global message_window, statistics_funcs
    all_statistic_types = ['mean','max','min','standard deviation','mode','variance',
                                   'median','range','percentile','skew','kurtosis','correlation','covariance',
                                   'moving average','Exponential-Weighted-Moving-Average','Z-scores','Cumulative Distribution Function',
                                   'Probability Density Function','MAD','M2','info entropy','auto-correlation', 'Jackknife-statistics', 'frequency count', 'Median Absolute Deviation Ratio',
                                   'linear-trend', 'trimmed-mean', 'F statistic', 'T statistic', 'P statistic', 'coefficient of variation','Pearson correlation coefficient']
    data_collecting_method = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect data?',
                                                        '.xlsx file', "by inputting the data manually")
    file_data = None
    if data_collecting_method:
        refresh_data = pyghelpers.textYesNoDialog(window, (0, 300, 600, 300), 'Do you want to refresh the data after each calculation?',
                                                        'yes', "no")
        # preload the data
        message_window.browser("Choose an Excel file for the data's source", [('EXCEL files', '.xlsx')])
        file_name = message_window.file_name
        if file_name == '':
            message_window.error("failed to process because of empty file name")
            return
        try:
            file = ExcelMgr(file_name)
            file_data = file.data
        except Exception as e:
            message_window.error('Failed to load data because of error:'+str(e))
            file_data = None
    else:
        refresh_data = True
    analyse_choice = CheckBox(32, all_statistic_types, 32,
                 window, clock, first_x=50, first_y=30, each_add_x=0, each_add_y=15, auto_adjust=False, buttons_adjust_length=40, bkg_width_adj=400,
                              background_color=(90, 90, 150))
    many_statistic_per_type = pyghelpers.textYesNoDialog(window, (0, 300, 700, 300), 'how many statistics of each type do you want to calculate?',
                                                        'Many(often use in data comparison)', "Only one each type")
    analyse_types = []
    if len(analyse_choice.clicked_choices) == 0 or type(analyse_choice.clicked_choices) == str:
        return
    if not many_statistic_per_type:
        analyse_types = analyse_choice.clicked_choices
    else:
        for curr_type in analyse_choice.clicked_choices:
            num = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'How many ' + all_statistic_types[curr_type] + ' do you want to calculate?',
                                              'OK',
                                              'CANCEL', backgroundColor=(90, 90, 150),
                                              promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            try:
                num = int(num)
            except Exception:
                message_window.error("Can't turn " + str(num) + ' into an integer')
                return
            if num < 0:
                message_window.error("You can't calculate negative statistics!")
                return
            else:
                for i in range(num):
                    analyse_types.append(i)

    if data_collecting_method:
        data = file_data
    else:
        data = loading_data(data_collecting_method, window, 'preload the data')
    if data is None or len(data) == 0:
        message_window.error('There is no available data, program exits.')
        return
    results = []
    total_num = len(analyse_types)
    curr_num = 1
    for statistic_type in analyse_types:
        if statistic_type not in [8, 11, 12, 13, 14, 27, 28, 29, 31]:#just need single group of data as input.
            results.append(all_statistic_types[statistic_type]+':'+str(statistics_funcs[statistic_type](data)))
        else:

            ########################### requires to input another number for use
            # percentile
            if statistic_type == 8:
                if data_collecting_method:
                    percent = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input the percent number, smaller or equal to 100 and bigger or equal to 0',
                                                                       [list_preview.draw], [list_preview.handle_event],
                                                                       'OK',
                                                                       'CANCEL', backgroundColor=(90, 90, 150),
                                                                       promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)
                else:
                    percent = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input the percent number, smaller or equal to 100 and bigger or equal to 0',[],[],
                                                                   'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                if percent is None:
                    message_window.error('no inputs is given')
                    return
                if not 0 <= percent <= 100:
                    message_window.error("the percent value is wrong:"+str(percent))
                    return
                results.append('percentile:'+str(percentile(data, percent)))
            # moving_average
            elif statistic_type == 13:
                if data_collecting_method:
                    window_size = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                               "input the window size,bigger than 0(it will traverse and take the average of each window-size's data)",
                                                               [list_preview.draw], [list_preview.handle_event],
                                                               'OK','CANCEL',allow_float=False, allow_negative=False, backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                else:
                    window_size = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), "input the window size,bigger than 0(it will traverse and take the average of each window-size's data)",
                                                                   [], [], 'OK','CANCEL', backgroundColor=(90, 90, 150),
                                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)
                if window_size is None:
                    message_window.error('no inputs is given')
                    return
                if not 0 < window_size:
                    message_window.error("the percent value is wrong:" + str(window_size))
                    return
                results.append('moving-average:' + str(moving_average(data, window_size)))
            # EWMA
            elif statistic_type == 14:
                if data_collecting_method:
                    alpha = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                   "input the weight(The closer the data is to the current loc, the greater the weight;and vice versa)",
                                                                   [list_preview.draw], [list_preview.handle_event],
                                                                   'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                else:
                    alpha = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), "input the weight(The closer the data is to the current loc, the greater the weight;and vice versa)",
                                                             [], [],'OK','CANCEL', backgroundColor=(90, 90, 150),
                                                             promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))

                if alpha is None:
                    message_window.error('no inputs is given')
                    return
                results.append('Exponential weighted moving average:' + str(EWMA(data, alpha)))

            ######################### requires to input another group of data
            # correlation
            elif statistic_type == 11:
                another_data = loading_data(data_collecting_method, window)
                if another_data is None or len(another_data) == 0:
                    message_window.error('There is no available data, program exits.')
                    return
                try:
                    results.append('correlation:'+str(correlation(data, another_data)))
                except Exception as e:
                    message_window.error(str(e)+'; failed to calculate correlation')
            # covariance
            elif statistic_type == 12:
                another_data = loading_data(data_collecting_method, window)
                if another_data is None or len(another_data) == 0:
                    message_window.error('There is no available data, program exits.')
                    return
                try:
                    results.append('covariance:' + str(covariance(data, another_data)))
                except Exception as e:
                    message_window.error(str(e) + '; failed to calculate covariance')
            # calculate_F_statistic
            elif statistic_type == 27:
                another_data = loading_data(data_collecting_method, window)
                if another_data is None or len(another_data) == 0:
                    message_window.error('There is no available data, program exits.')
                    return
                try:
                    results.append('F statistic:' + str(covariance(data, another_data)))
                except Exception as e:
                    message_window.error(str(e) + '; failed to calculate F statistic')
            # calculate_T_statistic
            elif statistic_type == 28:
                another_data = loading_data(data_collecting_method, window)
                if another_data is None or len(another_data) == 0:
                    message_window.error('There is no available data, program exits.')
                    return
                try:
                    results.append('T statistic:' + str(covariance(data, another_data)))
                except Exception as e:
                    message_window.error(str(e) + '; failed to calculate T statistic')
            # calculate_P_statistic
            elif statistic_type == 29:
                another_data = loading_data(data_collecting_method, window)
                if another_data is None or len(another_data) == 0:
                    message_window.error('There is no available data, program exits.')
                    return
                try:
                    results.append('P statistic:' + str(covariance(data, another_data)))
                except Exception as e:
                    message_window.error(str(e) + '; failed to calculate P statistic')
            # Pearson_correlation_coefficient
            elif statistic_type == 31:
                another_data = loading_data(data_collecting_method, window)
                if another_data is None or len(another_data) == 0:
                    message_window.error('There is no available data, program exits.')
                    return
                try:
                    results.append('Pearson correlation coefficient:' + str(covariance(data, another_data)))
                except Exception as e:
                    message_window.error(str(e) + '; failed to calculate Pearson correlation coefficient')

        if not curr_num == total_num:
            if refresh_data:
                # refresh the data
                if data_collecting_method:  # from excel files
                    message_window.browser("Choose an Excel file for the refreshing data's source; for the statistic "+str(all_statistic_types[statistic_type]), [('EXCEL files', '.xlsx')])
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
                    choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect data',
                                                        "by line(----)", 'by column(| | |)')

                    if not choice:  ####by column ################################################################################

                        arrange_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input arrange number',
                                                                   [list_preview.draw], [list_preview.handle_event],
                                                                   'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if arrange_num is None:
                            message_window.error('no inputs is given')
                            return
                        col_start_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                      'input cols start position of arrange (starts with 0)' + str(
                                                                          arrange_num), [list_preview.draw],
                                                                      [list_preview.handle_event], 'OK',
                                                                      'CANCEL', backgroundColor=(90, 90, 150),
                                                                      promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if col_start_num is None:
                            message_window.error('no inputs is given')
                            return
                        col_end_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                    'input cols end position of arrange (include)' + str(
                                                                        arrange_num),
                                                                    [list_preview.draw], [list_preview.handle_event],
                                                                    'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if col_end_num is None:
                            message_window.error('no inputs is given')
                            return
                        try:
                            data = []
                            num = 0
                            avail_num = 0
                            for i in file_data[col_start_num - 1:col_end_num]:
                                if type(i[arrange_num - 1]) in [int, float]:
                                    avail_num += 1
                                    data.append(i[arrange_num - 1])
                                num += 1
                            if avail_num != num:
                                message_window.warning('we found ' + str(
                                    num - avail_num) + ' valid data(s) in your file,we will ignore them(it)')
                            if len(data) == 0:
                                message_window.error('Exit because of no available data')
                                return
                        except IndexError as e:
                            message_window.error(str(e))
                            return

                    else:  ##### by line ################################################################################

                        line_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input line number',
                                                                [list_preview.draw], [list_preview.handle_event], 'OK',
                                                                'CANCEL', backgroundColor=(90, 90, 150),
                                                                promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if line_num is None:
                            message_window.error('no inpits is given')
                            return
                        line_start_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                      'input arrange start position("0"means arrange 1) of line ' + str(
                                                                          line_num), [list_preview.draw],
                                                                      [list_preview.handle_event], 'OK', 'CANCEL',
                                                                      backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                                      inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if line_start_num is None:
                            message_window.error('no inputs is given')
                            return
                        line_end_num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input arrange end position of line ' + str(line_num),
                                                                    [list_preview.draw], [list_preview.handle_event],
                                                                    'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

                        if line_end_num is None:
                            message_window.error('no inputs is given')
                            return
                        try:
                            num = 0
                            avail_num = 0
                            load_data = file_data[line_num][line_start_num:line_end_num + 1]
                            data = []
                            for i in load_data:
                                if type(i) in [int, float]:
                                    data.append(i)
                                    avail_num += 1
                                num += 1
                            if avail_num != num:
                                message_window.warning('we found ' + str(
                                    num - avail_num) + ' valid data in your file,we will ignore them')
                            if len(data) == 0:
                                return
                        except IndexError as e:
                            message_window.error(str(e))
                            return
                    list_preview = WindowListViewer(file_data, (1004, 410), window, (0, 200))
                else:
                    data = pyghelpers.textAnswerDialog(window, (200, 100, 500, 200),
                                                       "input you refreshing data split each other with ';'",
                                                       'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                       promptTextColor=(0, 0, 0),
                                                       inputTextColor=(0, 0, 0))
                    data = data.split(";")
                    data2 = []
                    unavailable = 0
                    for i in data:
                        try:
                            data2.append(float(i))
                        except Exception:
                            unavailable += 1
                    if unavailable != 0:
                        message_window.warning(
                            "there's " + str(unavailable) + ' unavailable data in your inputs, they will be ignored.')
                    data = data2
            else:
                if not curr_num == 1:
                    data = loading_data(data_collecting_method, window, reload_data=False,file_data=data)

        curr_num += 1
    pygame.draw.rect(window, (100, 149, 237), (0, 200, 1004, 410))
    answer_viewing = WindowListViewer([[curr] for curr in results], (1004, 410), window, (0, 200))
    copying_answer = textYesNoDialogEventProgressing(window, (0, 0, 1004, 200), 'Answer(s) are shown on the table below.',
                                        [answer_viewing.draw], [answer_viewing.handle_event],"Copy answer", 'Exit (all the answers will NOT BE SAVED!!!)')
    if copying_answer:
        pyperclip.copy(str(results)[1:-1])


def data_comparison(window, clock):
    global message_window
    data_num = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),  'how many times do you want to compare the data?',
                                            'OK','CANCEL', backgroundColor=(90, 90, 150),
                                            promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
    try:
        data_num = int(data_num)
    except:
        message_window.error('bad inputs for int:'+str(data_num))
        return
    if data_num < 0:
        message_window.error('times can not be negative')
        return
    charts_x_num = max([1,int(np.ceil(np.sqrt(data_num)))])
    charts_y_num = max([1,int(np.ceil(data_num / charts_x_num))])
    plt.close('all')
    fig = plt.figure()
    fig.clear()
    for i in range(data_num):
        data_collecting_method = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                            'how do you want to collect data?',
                                                            '.xlsx file', "by inputting the data manually")
        refresh_data = pyghelpers.textYesNoDialog(window, (0, 300, 600, 300),
                                                  'Do you want to refresh the data after each chart?',
                                                  'yes', "no")
        file_data = None
        if data_collecting_method:
            # preload the data
            message_window.browser("Choose an Excel file for the data's source", [('EXCEL files', '.xlsx')])
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
            finally:
                data = loading_data(data_collecting_method, window,' for preload', False,file_data)
        else:
            data = loading_data(data_collecting_method, window)

        if data is None or len(data) == 0:
            message_window.error('There is no available data, this time of comparison skips.')
            continue
        charts_type = CheckBox(8, ['hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'], 8,
                     window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30, buttons_adjust_length=0,
                     background_color=(90, 90, 150))
        curr_fig = fig.add_subplot(charts_y_num, charts_x_num, i+1)
        if len(charts_type.clicked_choices) == 0:
            message_window.error('no type of charts is selected.Current skips.')
            continue
        many_charts = pyghelpers.textYesNoDialog(window, (0, 300, 600, 300),
                                                 'How many charts of each type do you want to draw',
                                                 'many', "only one each type")
        chart_choices = []
        if many_charts:
            for curr in charts_type.clicked_choices:
                num = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'How many ' +
                                                  ['hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin',
                                                   'plot', 'scatter'][curr] + ' charts do you want to draw?',
                                                  'OK',
                                                  'CANCEL', backgroundColor=(90, 90, 150),
                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                try:
                    num = int(num)
                    if num <= 0:
                        message_window.error('you can not draw negative charts, and zero chart is meaningless')
                        return
                except:
                    message_window.error('bad inputs for int:'+str(num))
                    return
                for _ in range(num):chart_choices.append(curr)
        else:
            chart_choices = charts_type.clicked_choices
        start = True
        for curr_type in chart_choices:
            if start:
                start = False
            else:
                if refresh_data:
                    data = loading_data(data_collecting_method, window, ' for the refresh data')
                else:
                    data = loading_data(data_collecting_method, window, '',file_data, False)
                if data is None or len(data) == 0:
                    message_window.error('There is no available data, this time of comparison skips.')
                    continue


            if curr_type not in [0, 1, 2]:#requier to input two data
                if refresh_data:
                    data2 = loading_data(data_collecting_method, window, ' for '+['hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'][curr_type]+"'s second group of data")
                else:
                    data2 = loading_data(data_collecting_method, window, ' for ' +
                                         ['hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'][
                                             curr_type] + "'s second group of data", file_data=file_data, reload_data=False)

                if data2 is None or len(data2) == 0:
                    message_window.error('No data is selected.This time of comparison skips.')
                    continue
                if curr_type == 3:curr_fig.errorbar(data, data2)
                elif curr_type == 4:
                    bins = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'How many bins do you want',
                                                       'OK',
                                                       'CANCEL', backgroundColor=(90, 90, 150),
                                                       promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                    try:
                        bins = int(bins)
                        if bins <= 0:
                            message_window.error('you can not draw negative bins, and zero bin is meaningless')
                            return
                    except:
                        message_window.error('bad inputs for int:' + str(bins))
                        return
                    curr_fig.hist2d(data, data2, bins=bins)
                elif curr_type == 5:
                    bins = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'How many bins do you want',
                                                      'OK',
                                                      'CANCEL', backgroundColor=(90, 90, 150),
                                                      promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                    try:
                        bins = int(bins)
                        if bins <= 0:
                            message_window.error('you can not draw negative bins, and zero bin is meaningless')
                            return
                    except:
                        message_window.error('bad inputs for int:' + str(bins))
                        return
                    curr_fig.hexbin(data, data2, cmap='Blues', bins=bins)
                elif curr_type == 6:curr_fig.plot(data, data2)
                elif curr_type == 7:curr_fig.scatter(data, data2)
            else:
                if curr_type == 0:curr_fig.hist(data)
                elif curr_type == 1:curr_fig.box(data)
                elif curr_type == 3:curr_fig.violinplot(data)
    plt.legend()
    plt.tight_layout()
    plt.title('Data comparison')
    plt.show()


def normal_density(mean, sigma, x, drift=1.0):
    """
    :param drift: the data's mode
    :param mean:data's mean
    :param sigma:standard deviation
    :param x:the data
    :return:
    """
    return (1./(np.sqrt(2*np.pi)*sigma))*np.exp(-(x - mean) ** 2 / (2 * sigma ** 2)) * drift/(1/(sqrt(2*pi)*sigma))
    #max:1/(√(2π)σ) data max:drift


def IntervalClassification(data:list|tuple, IntervalNum:int=10, calculate_data:bool=True)-> list[list] | list[int]:
    data_max = np.max(data)
    data_min = np.min(data)
    ptp = data_max - data_min #极差
    width_per_interval = ptp / IntervalNum
    Intervals_data = [[] for _ in range(IntervalNum)]
    Intervals_num = [0 for _ in range(IntervalNum)]
    for curr in data:
        Intervals_data[ int((curr-data_min) // width_per_interval) - 1].append(curr)
        Intervals_num[ int((curr-data_min) // width_per_interval) - 1] += 1
    if calculate_data:
        return Intervals_data
    else:
        return Intervals_num


def data_distribution_analyse(data:list|tuple, bins:int=30, normal_curve_num:int=1000,show_mean=True, show_1_sigma=True, show_2_sigma=True, show_3_sigma=True, draw_normal=True):
    mean = np.mean(data)
    std = np.std(data)
    plt.close('all')
    fig = plt.figure()
    fig.clear()
    if draw_normal:
        normally_x = np.linspace(np.min(data), np.max(data), normal_curve_num)
        normally_y = normal_density(mean, std, normally_x, max(IntervalClassification(data, bins, False)))
        plt.plot(normally_x, normally_y, 'red')
        plt.legend(['normal distribution'])
    plt.hist(data, bins=bins, color='steelblue', edgecolor='k')
    plt.xlabel('numbers')
    plt.ylabel('frequency')
    if show_mean:
        plt.axvline(float(mean), color='red', linestyle='--')
    if show_1_sigma:
        plt.axvline(mean-std, color='y', linestyle='--')
        plt.axvline(mean+std, color='y', linestyle='--')
    if show_2_sigma:
        plt.axvline(mean-std*2, color='green', linestyle='--')
        plt.axvline(mean+std*2, color='green', linestyle='--')
    if show_3_sigma:
        plt.axvline(mean-std*3, color='k', linestyle='--')
        plt.axvline(mean+std*3, color='k', linestyle='--')
    plt.show()


def data_distribution(window, clock):
    data_collecting_method = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                        'how do you want to collect data?',
                                                        '.xlsx file', "by inputting the data manually")
    data = loading_data(data_collecting_method, window)
    if data is None or len(data) == 0:
        message_window.error('There is no available data, this time of comparison skips.')
        return
    draw_normal = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                        'do you want to draw the normal distribution?',
                                                        'yes', "no")
    charting_sigma_selector = CheckBox(4, ['1 sigma', '2 sigma', '3 sigma', 'mean'], 4,
                                      window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30,
                                      buttons_adjust_length=0, background_color=(90, 90, 150))
    charting_options = [False, False, False, False]
    if not len(charting_sigma_selector.clicked_choices) == 0:
        for _ in charting_sigma_selector.clicked_choices:charting_options[_]=True
    bins_num = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'how many bins do you want to draw?',
                                           'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
    try:
        bins_num = int(bins_num)
    except:
        message_window.error('bad inputs for int:'+str(bins_num))
        return
    data_distribution_analyse(data, bins=bins_num, draw_normal=draw_normal, show_mean=charting_options[3], show_1_sigma=charting_options[0],
                              show_2_sigma=charting_options[1], show_3_sigma=charting_options[2])


def load_data_2d(window, comments='', data_collecting_method=True, req: tuple[int, int] = None):
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
    plt.close('all')
    fig = plt.figure()
    fig.clear()

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
                z_data = load_data_2d(comments='z[shape:(' + str(len(x_data)) + ',' + str(len(y_data)) + ')]', data_collecting_method=data_collecting_method,
                                      req=(len(x_data), len(y_data)), window=window)
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
                z_data = load_data_2d('for the 2d data part('+str(len(x_data))+','+str(len(y_data))+')', data_collecting_method=data_collecting_method, req=(len(x_data), len(y_data)))
                if z_data is None:
                    message_window.error('No value is selected!, skip this draw');continue
                if len(z_data) != len(y_data) or len(z_data[0]) != len(x_data):
                    message_window.error('Dimension disagree:'+str(len(x_data))+'->'+str(len(z_data[0]))+';'+str(len(y_data))+'->'+str(len(z_data)))
                    continue
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
    window = pygame.display.set_mode((1004, 600))
    clock = pygame.time.Clock()

    #data_distribution(window, clock)
    data_comparison(window, clock)
    #data_analyze(window, clock)
    #data_visualize(window, clock, debug=True)
    pygame.quit()
    sys.exit(0)
