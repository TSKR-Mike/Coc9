import random
import sys

import pygame,pygwidgets, pyghelpers
from buttoncenter import ButtonCenter
import TableViewer
from EventPyghelpers import textAnswerDialogEventProgressing, textYesNoDialogEventProgressing, textNumberDialogEventProgressing
from ExcleMagr import ExcelMgr
from TableViewer.Table import WindowListViewer
import numpy as np
from checkbox import CheckBox
from statistics import Message_window


"""
矩阵运算法则包括矩阵的加法、减法、乘法以及转置等运算。

矩阵加法：只有行数和列数完全相同的矩阵才能进行加法运算。把两个矩阵对应位置的单个元素相加，得到的新矩阵就是矩阵加法的结果，且矩阵加法没有顺序，即 A+B=B+A。

矩阵减法：通常认为矩阵没有减法，若要与一个矩阵相减，在概念上是引入一个该矩阵的负矩阵，然后相加。A-B 是 A+(-B)的简写。

矩阵乘法：矩阵乘法并不是多个矩阵之和，它有自己的逻辑。假设 m 行 n 列的矩阵 A 和 r 行 v 列的矩阵 B 相乘得到矩阵 C，则首先矩阵 A 和矩阵 B 必须满足 n=r，也就是说，第一个矩阵的列数必须和第二个矩阵的行数相同。在运算时，第一个矩阵 A 的第 i 行的所有元素同第二个矩阵 B 第 j 列的元素对应相乘，并把相乘的结果相加，最终得到的值就是矩阵 C 的第 i 行第 j 列的值。这个过程用数学公式描述为：C(i，j)=A(i1，i2，i3……in)×B(j1，j2，j3……jv)，C(i，j)= i1×j1+i2 ×j2+i3×j3……+in×jv 。从矩阵的乘法运算过程可以看出，矩阵 A 和矩阵 B 相乘的产生的矩阵 C，必然是 m 行 v 列的。例如，一个 5×3 的矩阵同一个 3×7 的矩阵相乘，结果必然是产生一个 5×7 的矩阵。而一个 5×3 的矩阵同一个 5×7 的矩阵，则无法相乘。矩阵乘法同数字乘法不同，其运算的先后顺序十分敏感，矩阵 A 乘矩阵 B 的结果可能完全不同于矩阵 B 乘矩阵 A 的结果，有时甚至根本无法相乘。在图形变换时，经常用到多次变换，这会造成多个矩阵相乘。如果多个矩阵相乘，则等价于前两个矩阵相乘的结果再乘以第三个矩阵，以此向后类推。例如，假设 ABCD 都是矩阵，则 A×B×C×D=((A×B)×C)×D。为了方便操作，在图形学的实际应用中变换矩阵都是行数和列数相等的方阵。对于行和列不相等的矩阵，甚至要人为补足。
# 点乘（对应元素相乘）
result_multiply = np.multiply(matrix1, matrix2)
print("Element-wise Multiplication Result:\n", result_multipl

矩阵转置：将矩阵 A 的行换成同序号的列所得到的新矩阵称为矩阵 A 的转置矩阵。

需要注意的是，矩阵运算有着严格的规则和条件，只有在满足相应条件的情况下，才能进行有效的运算。在实际应用和学习中，需要准确理解和掌握这些规则，以避免错误的运算和结果。
"""

message_window = Message_window()

def random_string(length:int):
    string = ''
    for _ in range(length):
        string += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return string

def loading_matrix(data_collecting_method, window, names,comments:str=''):
    global message_window
    data = []
    matrix = []
    matrix_name = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'input the name of the matrix', 'OK',
                                                   'CANCEL', backgroundColor=(90, 90, 150),
                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
    if matrix_name is None:
        message_window.warning('you did NOT select a name for the matrix!system will create a 10-length string randomly')
        matrix_name = random_string(10)
    if matrix_name.count('>') or matrix_name.count('|') or matrix_name.count(';'):
        message_window.error('you matrix name contains illegal chars:">","|" or ";"')
        return
    if matrix_name in names:
        message_window.warning('you name is the same as some in all matrixs.system will add some random chars')
        matrix_name += random_string(2)
        while matrix_name in names:
            matrix_name = matrix_name[0:len(matrix_name)-2]
            matrix_name += random_string(2)
    matrix.append(matrix_name)
    if data_collecting_method:#from excel files
        message_window.browser("Choose an Excel file for the matrix's source", [('EXCEL files', '.xlsx')])
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

        arrange_start = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input starting arrange number',
                                                   [list_preview.draw], [list_preview.handle_event], 'OK',
                                                   'CANCEL', backgroundColor=(90, 90, 150),
                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

        if arrange_start is None:
            message_window.error('no inputs is given')
            return
        arrange_end = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input ending arrange number(included)',
                                                   [list_preview.draw], [list_preview.handle_event], 'OK',
                                                   'CANCEL', backgroundColor=(90, 90, 150),
                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

        if arrange_end is None:
            message_window.error('no inputs is given')
            return

        column_start = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input starting column number',
                                                       [list_preview.draw], [list_preview.handle_event], 'OK',
                                                       'CANCEL', backgroundColor=(90, 90, 150),
                                                       promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

        if column_start is None:
            message_window.error('no inputs is given')
            return
        column_end = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input ending column number(included)',
                                                       [list_preview.draw], [list_preview.handle_event], 'OK',
                                                       'CANCEL', backgroundColor=(90, 90, 150),
                                                       promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

        if column_end is None:
            message_window.error('no inputs is given')
            return

        try:
            if not choice:  ####by column ################################################################################
                file_data = [curr_line[column_start:column_end+1] for curr_line in file_data]
                array = np.array(file_data)
                array = np.transpose(array)
                array = array.tolist()
                data = []
                for line in array:
                    data.append(line[arrange_start:arrange_end+1])

            else: ##### by line ################################################################################
                file_data = file_data[arrange_start:arrange_end+1]
                data = []
                for line in file_data:
                    data.append(line[column_start:column_end+1])
        except Exception as e:
            message_window.error(str(e));return
    else:
        num = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'How many arranges do you want?',[], []
                                          ,'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                          promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)

        if num is None:
            message_window.error('no inputs is given')
            return
        if num == 0:
            message_window.error('zero arrange is meaningless')
            return
        for i in range(num):
            curr_data = pyghelpers.textAnswerDialog(window, (200, 100, 500, 200),
                                               "input you line of data split each other with ';'",
                                               'OK', 'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                               inputTextColor=(0, 0, 0))
            if curr_data is None:
                message_window.error('No inputs is given.This line is skipped.')
                continue
            curr_data = curr_data.split(";")
            data2 = []
            unavailable = 0
            for i in curr_data:
                try:
                    data2.append(float(i))
                except Exception:
                    unavailable += 1
            if unavailable != 0:
                message_window.warning("there's "+str(unavailable)+' unavailable data in your inputs, they will be ignored.')
            curr_data = data2
            data.append(curr_data)
        first_length = len(data[0])
        if not all(len(lst) == first_length for lst in data):
            message_window.error('the input is NOT form a matrix')
            return
    if len(data) == 0:
        message_window.error('The matrix is None, program exits.')
        return
    matrix.append(data)
    return [matrix]

def MatrixDotMultiplication(matrix1:np.array, matrix2:np.array):
    if not matrix1.shape[1] != matrix2.shape[0]:
        return np.dot(matrix1, matrix2)
    else:
        message_window.error("the dimension 1 of the first matrix ("+str(matrix1.shape[1])+")does not equal to the dimension 0 of the second matrix("+str(matrix2.shape[0])+')')

def MatrixCrossProduct(matrix1:np.array, matrix2:np.array):
    if matrix1.shape[0] == matrix2.shape[0] and matrix1.shape[1] == matrix2.shape[1]:
        return np.multiply(matrix1, matrix2)
    else:
        message_window.error("the dimensions of the first matrix (" + str(
            matrix1.shape) + ")do not equal to the dimensions of the second matrix(" + str(
            matrix2.shape) + ')')

def MatrixAddition(matrix1:np.array, matrix2:np.array):
    if matrix1.shape[0] == matrix2.shape[0] and matrix1.shape[1] == matrix2.shape[1]:
        return np.add(matrix1, matrix2)
    else:
        message_window.error("the dimensions of the first matrix (" + str(
            matrix1.shape) + ")do not equal to the dimensions of the second matrix(" + str(
            matrix2.shape) + ')')

def MatrixSubtract(matrix1:np.array, matrix2:np.array):
    if matrix1.shape[0] == matrix2.shape[0] and matrix1.shape[1] == matrix2.shape[1]:
        return np.subtract(matrix1, matrix2)

def MatrixTransform(matrix1:np.array):
    return np.transpose(matrix1)

def load_matrix_from_CocMatrixInfo(file_name, names):
    if file_name.split('.')[-1] != 'CocMatrixInfo':
        message_window.error('unsupported type:'+str(file_name.split('.')[-1])+';except type:CocMatrixInfo')
    with open(file_name, 'r') as matrix_file:
        try:
            all_matrix = []
            file_data = matrix_file.readlines()
            for curr in file_data:
                name, actual_data_str = curr.split('>')[0], curr.split('>')[1]
                if name in names:
                    message_window.warning('the name is the same as some in all the matrix, system will add some random chars')
                    name += random_string(2)
                    while name in names:
                        name = name[0:len(name)-2]
                        name += random_string(2)
                curr_matrix = []
                all_curr_lines = actual_data_str.split('|')
                for matrix_line in all_curr_lines:
                    curr_matrix.append([float(item) for item in matrix_line.split(';')])
                all_matrix.append([name, curr_matrix])
            return all_matrix
        except Exception as e:
            raise e

def write_matrix_to_CocMatrixInfo(file_name, matrix):
    """
    :param file_name: str
    :param matrix: [( <matrix name>, <data -> list[list[int...]]> ), ...]
    :return:
    """
    if len(matrix) == 0:return
    with open(file_name, 'w') as matrix_file:
        try:
            for matrix in matrix:
                name = matrix[0]
                matrix_file.write(str(name)+'>')
                data = matrix[1]
                data_str = ''
                data_length = len(data)
                for line, line_index in zip(data, range(len(data))):
                    curr_line_str = ''
                    line_length = len(line)
                    for item, index in zip(line, range(len(line))):
                        curr_line_str += str(item)
                        if index != line_length - 1:
                            curr_line_str += ';'
                    data_str += curr_line_str
                    if line_index != data_length - 1:
                        data_str += '|'
                matrix_file.write(data_str+'\n')

        except Exception as e:
            raise e

def load_matrix_3_choices(window, clock, names,debug=False):
    loading_type_selector = CheckBox(3, ['input manually', 'load from .xlsx files', 'load from .CocMatrixInfo files'], 1,
                                      window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30,
                                      buttons_adjust_length=0, background_color=(90, 90, 150))
    if loading_type_selector.clicked_choices == 'cancel':
        message_window.error('no inputs is given')
        return
    if len(loading_type_selector.clicked_choices) != 0:
        choice = loading_type_selector.clicked_choices[0]
        if choice <= 1:
            return loading_matrix(choice, window, names)
        else:
            try:
                message_window.select_file(dir='MatrixFiles')
                file_name = message_window.file_name
                return load_matrix_from_CocMatrixInfo(file_name, names)
            except Exception as e:
                if debug:
                    raise e
                return

def select_curr_matrix(window, all_matrix, comments=''):
    if len(all_matrix) == 0:
        message_window.error('there is no available matrix')
        return
    drawing_data = []
    for curr in all_matrix:
        _ = [(str(np.array(curr[1]).shape))]
        _.insert(0, curr[0])
        drawing_data.append(_)
    drawing_data.insert(0, ['name', 'size'])
    for index in range(len(all_matrix) + 1):
        if index != 0:
            drawing_data[index].insert(0, index - 1)
        else:
            drawing_data[0].insert(0, '#')
    matrix_selection = WindowListViewer(drawing_data, (1004, 304), window, (0, 190), auto_heading=False)
    select_by_index = textYesNoDialogEventProgressing(window, (0, 0, 1004, 190),
                                                      'How do you want to select the complex' + comments,
                                                      [matrix_selection.draw], [matrix_selection.handle_event],
                                                      'By index',
                                                      'By name', backgroundColor=(90, 90, 150))
    if select_by_index:
        matrix_index = textAnswerDialogEventProgressing(window, (0, 0, 1004, 190), 'input matrix index'+comments,
                                                         [matrix_selection.draw], [matrix_selection.handle_event], 'OK',
                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                         promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        if matrix_index is None:
            message_window.error('exit because of empty input')
            return
        try:
            matrix_index = int(matrix_index)
        except:
            message_window.error('bad inputs for int:"'+str(matrix_index)+'"')
            return
        if 0 <= matrix_index < len(all_matrix):
            return all_matrix[matrix_index]
        else:
            message_window.error('Index out of range: get ' + str(matrix_index) +' instead of a number between 0 and ' + str(len(all_matrix) - 1))
            return
    else:
        name = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                           'input the name of the matrix', 'OK',
                                           'CANCEL', backgroundColor=(90, 90, 150),
                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        all_names = [curr[0] for curr in all_matrix]
        if name not in all_names:
            message_window.error('the name "' + str(name) + '" is NOT included in all matrix')
            return
        for curr_complex in all_matrix:
            if curr_complex[0] == name:
                return curr_complex


class subWindow:
    def __init__(self, window, loc, length, height, bkg_colour=(0, 191, 255), title='SubWindow'):
        self.window, self.loc, self.length, self.height, self.bkg_colour, self.title = window, loc, length, height, bkg_colour, title
        self.cancel_button = pygwidgets.TextButton(self.window, (loc[0]+length-60, loc[1]), 'x', 60, 30,
                                                   upColor=pygwidgets.PYGWIDGETS_NORMAL_GRAY,downColor=(255, 0, 0),overColor=(255, 0, 0))
        self.minimize_button = pygwidgets.TextButton(self.window, (loc[0] + length - 120, loc[1]), '-', 60, 30)
        self.title_bkg = pygwidgets.TextButton(self.window, (loc[0], loc[1]), '', length, 30, upColor=(135, 206, 250), downColor=(135, 206, 250), overColor=(135, 206, 250))
        self.title_view = pygwidgets.DisplayText(self.window, (loc[0]+3, loc[1]), title, fontName='fonts/JetBrainsMono-Light.ttf')

    def draw(self):
        while True:
            pygame.draw.rect(self.window, self.bkg_colour, (self.loc[0], self.loc[1], self.length, self.height))
            for event in pygame.event.get():
                if self.cancel_button.handleEvent(event):
                    return
                if self.minimize_button.handleEvent(event):
                    return
            self.title_bkg.draw()
            self.title_view.draw()
            self.cancel_button.draw()
            self.minimize_button.draw()
            pygame.display.update()


class MatrixUi(subWindow):


    def __init__(self, window, clock, loc, length, height, bkg_colour=(0, 191, 255), all_data=({}, [], None)):
        super().__init__(window, loc, length, height, bkg_colour, 'Matrix')
        self.curr_matrix_preview = None
        self.all_matrix_preview = None
        self.clock = clock
        self.all_matrix_dict = all_data[0]
        # {<key:matrix name>:(np.array->data,length, height),...}
        self.all_matrix_data = all_data[1]
        # [[name, data], ...]
        self.curr_matrix = all_data[2]
        #[name, data]
        self.all_buttons_line1 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 6,
                     ['Select Matrix', 'Matrix Addition', 'Matrix Subtract', 'Dot Multiplication', 'Cross Product', 'Transform'], self.window, 150, 60, 0, 30, 152, 0, font='fonts/JetBrainsMono-Light.ttf', font_size=13,
                     callbacks=None)
        self.all_buttons_line2 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 6,
                                              ['Extract Matrix', 'Insert Matrix', 'Clear selection', 'Modify Matrix', 'Copy Matrix', 'Remove matrix'], self.window, 150, 60, 0, 90, 152, 0,
                                              font='fonts/JetBrainsMono-Light.ttf', font_size=13,
                                              callbacks=None)
        self.curr_matrix_title = 'No matrix is selected'
        self.all_matrix_preview_title = pygwidgets.TextButton(self.window, (0, 150), 'All matrix', fontName='fonts/JetBrainsMono-Light.ttf', width=304,
                                                              upColor=(135, 206, 250), downColor=(135, 206, 250), overColor=(135, 206, 250))
        self.curr_matrix_preview_title = pygwidgets.TextButton(self.window, (304, 150), self.curr_matrix_title,
                                                              fontName='fonts/JetBrainsMono-Light.ttf', width=700,
                                                              upColor=(135, 206, 250), downColor=(135, 206, 250), overColor=(135, 206, 250))

        self.update = False

    def draw(self):
        while True:
            pygame.draw.rect(self.window, self.bkg_colour, (self.loc[0], self.loc[1], self.length, self.height))# draw the bkground
            pygame.draw.line(self.window, (135, 206, 250), (304, 150), (304, 610), width=3)# draw the split line
            self.all_matrix_data = [list(i) for i in self.all_matrix_data]
            if len(self.all_matrix_data) != 0:
                if type(self.all_matrix_preview) != TableViewer.Table.WindowListViewer or self.update:
                    drawing_data = []
                    for curr in self.all_matrix_data:
                        _ = [(str(np.array(curr[1]).shape))]
                        _.insert(0, curr[0])
                        drawing_data.append(_)
                    drawing_data.insert(0, ['name', 'size'])
                    self.all_matrix_preview = WindowListViewer(drawing_data, (304, 460), self.window, (0, 190), auto_heading=False)
            else:
                self.all_matrix_preview = pygwidgets.DisplayText(self.window, (70, 345), 'Nothing to show', fontName='fonts/JetBrainsMono-Light.ttf')

            if self.curr_matrix is None:
                self.curr_matrix_title = 'No matrix is selected'
                self.curr_matrix_preview = pygwidgets.DisplayText(self.window, (540, 345), 'Nothing to show', fontName='fonts/JetBrainsMono-Light.ttf')
            else:
                if type(self.curr_matrix_preview) != TableViewer.Table.WindowListViewer or self.update:
                    self.curr_matrix_preview = WindowListViewer(self.curr_matrix[1], (700, 420), self.window, (304, 190))
                    self.curr_matrix_title = self.curr_matrix[0]
                    self.curr_matrix_preview_title = pygwidgets.TextButton(self.window, (304, 150), self.curr_matrix_title,
                                                                               fontName='fonts/JetBrainsMono-Light.ttf',
                                                                               width=700,
                                                                               upColor=(135, 206, 250),
                                                                               downColor=(135, 206, 250),
                                                                               overColor=(135, 206, 250))

            #draw curr matrix previews
            self.curr_matrix_preview.draw()
            self._cover_curr_preview()

            #draw others
            self.curr_matrix_preview_title.draw()
            self.all_matrix_preview.draw()
            pygame.draw.rect(self.window, self.bkg_colour, (0, 0, 304, 190))
            self.all_matrix_preview_title.draw()
            self.title_bkg.draw()
            self.title_view.draw()
            self.all_buttons_line1.drawAllButtons()
            self.all_buttons_line2.drawAllButtons()
            self.cancel_button.draw()
            self.minimize_button.draw()

            if self.update:self.update = False
            for event in pygame.event.get():
                if type(self.curr_matrix_preview) == TableViewer.Table.WindowListViewer:self.curr_matrix_preview.handle_event(event)
                if type(self.all_matrix_preview) == TableViewer.Table.WindowListViewer:self.all_matrix_preview.handle_event(event)
                for curr in self.all_buttons_line1.Buttons:
                    if curr.handleEvent(event):
                        INDEX = self.all_buttons_line1.Buttons.index(curr)
                        if INDEX == 0:
                            #select matrix
                            self.select_matrix()
                        elif INDEX == 1:
                            #matrix addition
                            self.addition()
                        elif INDEX == 2:
                            #matrix subtraction
                            self.subtraction()
                        elif INDEX ==3:
                            #matrix dot multiplication
                            self.DotMultiplication()
                        elif INDEX == 4:
                            #matrix cross product
                            self.CrossProduct()
                        elif INDEX == 5:
                            #matrix transform
                            self.Transform()

                for curr in self.all_buttons_line2.Buttons:
                    if curr.handleEvent(event):
                        INDEX = self.all_buttons_line2.Buttons.index(curr)
                        if INDEX == 0:
                            #extract matrix
                            self.extract_matrix()
                        elif INDEX == 1:
                            #insert matrix
                            self.insert_matrix()
                        elif INDEX == 2:
                            #clear current matrix
                            self.clear_curr_matrix()
                        elif INDEX == 3:
                            #modify matrix
                            self.change_curr_matrix()
                        elif INDEX == 4:
                            #copy matrix
                            self.copy_matrix()
                        elif INDEX == 5:
                            #remove matrix
                            if self.curr_matrix is None:
                                message_window.error('no current matrix is selected!')
                                self.select_matrix()
                                return
                            name = self.curr_matrix[0]
                            Index = self.all_matrix_data.index(self.curr_matrix)
                            del self.all_matrix_data[Index]
                            del self.all_matrix_dict[name]
                            self.curr_matrix = None
                            self.update = True
                if self.cancel_button.handleEvent(event):
                    if message_window.question(question='If leave now, all you data WILL NOT BE SAVED. Do you want to save them?'):
                        self.extract_matrix()
                    return {}, [], None

                if self.minimize_button.handleEvent(event):
                    return self.all_matrix_dict,self.all_matrix_data,self.curr_matrix
            pygame.display.update()

    def load_matrix(self):
        matrix = load_matrix_3_choices(self.window, self.clock, [i[0] for i in self.all_matrix_data])
        if matrix is not None:
            for curr in matrix:
                name = curr[0]
                data = curr[1]
                array = np.array(data)
                self.all_matrix_dict[str(name)] = data
                self.all_matrix_data.append([name, data])
                self.update = True

    def extract_matrix(self):
        file_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200), 'input file name(will be saved in "/MatrixFiles" dir)', 'OK',
                                                        'CANCEL', backgroundColor=(90, 90, 150),
                                                        promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        if file_name is None:
            message_window.error('no file name is given')
            return
        file_name = str(file_name)
        write_matrix_to_CocMatrixInfo("MatrixFiles/"+file_name+'.CocMatrixInfo', self.all_matrix_data)
        message_window.message('extract completed')

    def select_matrix(self, fresh_curr_matrix=True, comments=''):
        m = select_curr_matrix(self.window, self.all_matrix_data, comments)
        self.update = True
        if fresh_curr_matrix:
            self.curr_matrix = m
        else:
            return m

    def insert_matrix(self):
        all_matrix = load_matrix_3_choices(self.window, self.clock, [i[0] for i in self.all_matrix_data])
        if all_matrix is None or len(all_matrix) == 0:
            return
        for name, value in all_matrix:
            if name in self.all_matrix_dict.keys():
                name += random_string(2)
                while name in self.all_matrix_dict.keys():
                    name = name[0:-1]
                    name += random_string(2)
        for curr_matrix in all_matrix:
            self.all_matrix_dict[curr_matrix[0]] = curr_matrix[1]
            self.all_matrix_data.append(curr_matrix)
            self.update = True
        message_window.message('insert completed')

    def clear_curr_matrix(self):self.curr_matrix = None;self.update = True

    def addition(self):
        if self.curr_matrix is None:
            self.select_matrix(comments='for addition(1)')
        other = self.select_matrix(fresh_curr_matrix=False,comments='for addition(2)')
        quit = False
        if self.curr_matrix is None:
            message_window.error('the first matrix of the addition did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second matrix of addiction did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            matrix_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                    'input matrix name', 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if matrix_name is not None:
                if '|' in matrix_name or '>' in matrix_name or ';' in matrix_name:
                    message_window.warning("you matrix name includes '|', '>' or ';', which is(are) not allowed. system will create one randomly")
                    matrix_name = random_string(5)
                if matrix_name in self.all_matrix_dict.keys():
                    message_window.warning('the name of the matrix is included,system will add some random chars')
                    new_name = (matrix_name + random_string(5))
                    while new_name in self.all_matrix_dict.keys():
                        new_name = (matrix_name + random_string(5))
                    matrix_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one radomly')
                matrix_name = random_string(7)
                while matrix_name in self.all_matrix_dict.keys():
                    matrix_name = random_string(7)
            try:
                answer = MatrixAddition(np.array(self.curr_matrix[1]), np.array(other[1]))
                answer = answer.tolist()
                self.all_matrix_data.append((matrix_name, answer))
                self.all_matrix_dict[matrix_name] = answer
                self.update = True
            except Exception as e:
                message_window.error('can not add the two matrix because of the error:'+str(e))
                return
            
    def subtraction(self):
        if self.curr_matrix is None:
            self.select_matrix(comments='for subtraction(1)')
        other = self.select_matrix(fresh_curr_matrix=False,comments='for subtraction(2)')
        quit = False
        if self.curr_matrix is None:
            message_window.error('the first matrix of the subtraction did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second matrix of subtraction did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            matrix_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                    'input matrix name', 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if matrix_name is not None:
                if '|' in matrix_name or '>' in matrix_name or ';' in matrix_name:
                    message_window.warning("you matrix name includes '|', '>' or ';', which is(are) not allowed. system will create one randomly")
                    matrix_name = random_string(5)
                if matrix_name in self.all_matrix_dict.keys():
                    message_window.warning('the name of the matrix is included,system will add some random chars')
                    new_name = (matrix_name + random_string(5))
                    while new_name in self.all_matrix_dict.keys():
                        new_name = (matrix_name + random_string(5))
                    matrix_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one radomly')
                matrix_name = random_string(7)
                while matrix_name in self.all_matrix_dict.keys():
                    matrix_name = random_string(7)
            try:
                answer = MatrixSubtract(np.array(self.curr_matrix[1]), np.array(other[1]))
                answer = answer.tolist()
                self.all_matrix_data.append((matrix_name, answer))
                self.all_matrix_dict[matrix_name] = answer
                self.update = True
            except Exception as e:
                message_window.error('can not add the two matrix because of the error:'+str(e))
                return

    def DotMultiplication(self):
        if self.curr_matrix is None:
            self.select_matrix(comments='for Dot Multiplication(1)')
        other = self.select_matrix(fresh_curr_matrix=False,comments='for Dot Multiplication(2)')
        quit = False
        if self.curr_matrix is None:
            message_window.error('the first matrix of the Dot Multiplication did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second matrix of Dot Multiplication did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            matrix_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                    'input matrix name', 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if matrix_name is not None:
                if '|' in matrix_name or '>' in matrix_name or ';' in matrix_name:
                    message_window.warning("you matrix name includes '|', '>' or ';', which is(are) not allowed. system will create one randomly")
                    matrix_name = random_string(5)
                if matrix_name in self.all_matrix_dict.keys():
                    message_window.warning('the name of the matrix is included,system will add some random chars')
                    new_name = (matrix_name + random_string(5))
                    while new_name in self.all_matrix_dict.keys():
                        new_name = (matrix_name + random_string(5))
                    matrix_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one radomly')
                matrix_name = random_string(7)
                while matrix_name in self.all_matrix_dict.keys():
                    matrix_name = random_string(7)
            try:
                answer = MatrixDotMultiplication(np.array(self.curr_matrix[1]), np.array(other[1]))
                answer = answer.tolist()
                self.all_matrix_data.append((matrix_name, answer))
                self.all_matrix_dict[matrix_name] = answer
                self.update = True
            except Exception as e:
                message_window.error('can not add the two matrix because of the error:'+str(e))
                return

    def CrossProduct(self):
        if self.curr_matrix is None:
            self.select_matrix(comments='for Cross Product(1)')
        other = self.select_matrix(fresh_curr_matrix=False,comments='for Cross Product(2)')
        quit = False
        if self.curr_matrix is None:
            message_window.error('the first matrix of the Cross Product did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second matrix of Cross Product did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            matrix_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                    'input matrix name', 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if matrix_name is not None:
                if '|' in matrix_name or '>' in matrix_name or ';' in matrix_name:
                    message_window.warning("you matrix name includes '|', '>' or ';', which is(are) not allowed. system will create one randomly")
                    matrix_name = random_string(5)
                if matrix_name in self.all_matrix_dict.keys():
                    message_window.warning('the name of the matrix is included,system will add some random chars')
                    new_name = (matrix_name + random_string(5))
                    while new_name in self.all_matrix_dict.keys():
                        new_name = (matrix_name + random_string(5))
                    matrix_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one radomly')
                matrix_name = random_string(7)
                while matrix_name in self.all_matrix_dict.keys():
                    matrix_name = random_string(7)
            try:
                answer = MatrixCrossProduct(np.array(self.curr_matrix[1]), np.array(other[1]))
                answer = answer.tolist()
                self.all_matrix_data.append((matrix_name, answer))
                self.all_matrix_dict[matrix_name] = answer
                self.update = True
            except Exception as e:
                message_window.error('can not add the two matrix because of the error:'+str(e))
                return

    def Transform(self):
        if self.curr_matrix is None:
            self.select_matrix(comments='for Transform')
        if self.curr_matrix is None:
            message_window.error('the matrix of the Transform did NOT select correctly')
            return
        else:
            matrix_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                    'input matrix name', 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if matrix_name is not None:
                if '|' in matrix_name or '>' in matrix_name or ';' in matrix_name:
                    message_window.warning("you matrix name includes '|', '>' or ';', which is(are) not allowed. system will create one randomly")
                    matrix_name = random_string(5)
                if matrix_name in self.all_matrix_dict.keys():
                    message_window.warning('the name of the matrix is included,system will add some random chars')
                    new_name = (matrix_name + random_string(5))
                    while new_name in self.all_matrix_dict.keys():
                        new_name = (matrix_name + random_string(5))
                    matrix_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one radomly')
                matrix_name = random_string(7)
                while matrix_name in self.all_matrix_dict.keys():
                    matrix_name = random_string(7)
            try:
                answer = MatrixTransform(np.array(self.curr_matrix[1]))
                answer = answer.tolist()
                self.all_matrix_data.append((matrix_name, answer))
                self.all_matrix_dict[matrix_name] = answer
                self.update = True
            except Exception as e:
                message_window.error('can not add the two matrix because of the error:'+str(e))
                return

    def change_curr_matrix(self):
        if self.curr_matrix is None:
            message_window.error('no matrix is selected!');return
        changing_type_selector = CheckBox(4,
                                         ['by line(---)', 'by column(|||)', 'by cells(x,y)','RENAME'],
                                         1,
                                         self.window, self.clock, first_x=60, first_y=100, each_add_x=0, each_add_y=30,
                                         buttons_adjust_length=0, background_color=(90, 90, 150))
        if len(changing_type_selector.clicked_choices) == 0 or type(changing_type_selector.clicked_choices) == str:return
        choice = changing_type_selector.clicked_choices[0]

        if choice == 0:
            #by line
            changing_by_line_type_selector = CheckBox(3,
                                              ['add one more line', 'delete a line', 'modify an line'],
                                              1,
                                              self.window, self.clock, first_x=60, first_y=100, each_add_x=0, each_add_y=30,
                                              buttons_adjust_length=0, background_color=(90, 90, 150))
            if len(changing_by_line_type_selector.clicked_choices) == 0:message_window.error('no one selected!');return
            else:
                changing_by_line_type_selector = changing_by_line_type_selector.clicked_choices[0]

            if changing_by_line_type_selector in [1, 2]:
                line_index = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200), 'input the index of the matrix'+str(self.curr_matrix[0])+'(by line),between 0 and '+str(len(self.curr_matrix)-1), 'OK',
                                                          'CANCEL', backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))

                try:
                    line_index = int(line_index)
                    if not 0 <= line_index <= len(self.curr_matrix[1][0])-1:
                        message_window.error('the index:'+str(line_index)+'is NOT between 0 and '+str(len(self.curr_matrix[1][0])-1))
                        return
                except:
                    message_window.error('bad inputs for int:'+str(line_index))
                    return

            if changing_by_line_type_selector in [0, 2]:
                line_data = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                         'input the data(split with ";")(total of '+str(len(self.curr_matrix[1][0])), 'OK',
                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                         promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                if line_data is None:message_window.error('no inputs!');return
                line_data = line_data.split(';')
                if len(line_data) > len(self.curr_matrix[1][0]):
                    message_window.warning('you input is '+str(len(line_data))+', which is higher than others.system will cut them into right size automatically')
                    line_data = line_data[0:len(self.curr_matrix[1][0])]
                elif len(line_data) < len(self.curr_matrix[1][0]):
                    message_window.warning('you input is ' + str(
                        len(line_data)) + ', which is lower than others.system will add "0" to right size automatically')
                    line_data.extend([0 for _ in range(len(self.curr_matrix[1][0])-len(line_data))])
            name = self.curr_matrix[0]
            if changing_by_line_type_selector == 0:#add
                self.all_matrix_dict[name][1].append(line_data)
                self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)][1].append(line_data)
                self.curr_matrix[1].append(line_data)
            elif changing_by_line_type_selector == 1:#delete
                del self.all_matrix_dict[name][1][line_index]
                del self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)][1][line_index]
                del self.curr_matrix[1][line_index]
            elif changing_by_line_type_selector == 2:#modify
                self.all_matrix_dict[name][1][line_index] = line_data
                self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)][1][line_index] = line_data
                self.curr_matrix[1][line_index] = line_data
        elif choice == 1:
            #by column
            changing_by_column_type_selector = CheckBox(3,['add one more column', 'delete a colum', 'modify an column'],
                                                      1,self.window, self.clock, first_x=60, first_y=100, each_add_x=0,
                                                      each_add_y=30,buttons_adjust_length=0, background_color=(90, 90, 150))
            if len(changing_by_column_type_selector.clicked_choices) == 0: message_window.error('no one selected!');return
            else:
                changing_by_column_type_selector = changing_by_column_type_selector.clicked_choices[0]
            name = self.curr_matrix[0]
            
            if changing_by_column_type_selector in [1, 2]:
                column_index = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                         'input the index of the matrix' + str(
                                                             self.curr_matrix[0]) + '(by column),between 0 and ' + str(
                                                             len(self.curr_matrix) - 1), 'OK',
                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                         promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))

                try:
                    column_index = int(column_index)
                    if not 0 <= column_index <= len(self.curr_matrix[1]) - 1:
                        message_window.error(
                            'the index:' + str(column_index) + 'is NOT between 0 and ' + str(len(self.curr_matrix[1]) - 1))
                        return
                except:
                    message_window.error('bad inputs for int:' + str(column_index))
                    return

            if changing_by_column_type_selector in [0, 2]:
                column_data = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                        'input the data(split with ";")(total of ' + str(
                                                            len(self.curr_matrix[1])), 'OK',
                                                        'CANCEL', backgroundColor=(90, 90, 150),
                                                        promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                if column_data is None: message_window.error('no inputs!');return
                column_data = column_data.split(';')
                if len(column_data) > len(self.curr_matrix[1]):
                    message_window.warning('you input is ' + str(
                        len(column_data)) + ', which is higher than others.system will cut them into right size automatically')
                    column_data = column_data[0:len(self.curr_matrix[1])]
                elif len(column_data) < len(self.curr_matrix[1]):
                    message_window.warning('you input is ' + str(
                        len(column_data)) + ', which is lower than others.system will add "0" to right size automatically')
                    column_data.extend([0 for _ in range(len(self.curr_matrix[1]) - len(column_data))])

            if changing_by_column_type_selector == 0:#add
                index_ = 0
                for line in (self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)]):
                    self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)][index_].append(column_data)
                    index_ += 1
                index_ = 0
                for line in (self.all_matrix_dict[name]):
                    self.all_matrix_dict[name][index_].append(column_data)
                    index_ += 1
                index_ = 0
                for line in (self.curr_matrix[1]):
                    self.curr_matrix[1][index_].append(column_data)
                    index_ += 1
            elif changing_by_column_type_selector == 1:#delete
                index_ = 0
                for line in (self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)]):
                    del self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)][index_][column_index]
                    index_ += 1
                index_ = 0
                for line in (self.all_matrix_dict[name]):
                    del self.all_matrix_dict[name][index_][column_index]
                    index_ += 1
                index_ = 0
                for line in (self.curr_matrix[1]):
                    del self.curr_matrix[1][index_][column_index]
                    index_ += 1
            elif changing_by_column_type_selector == 2:#modify
                index_ = 0
                for line in (self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)]):
                    self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)][index_][column_index] = column_data[index_]
                    index_ += 1
                index_ = 0
                for line in (self.all_matrix_dict[name]):
                    self.all_matrix_dict[name][index_][column_index] = column_data[index_]
                    index_ += 1
                index_ = 0
                for line in (self.curr_matrix[1]):
                    self.curr_matrix[1][index_][column_index] = column_data[index_]
                    index_ += 1
        elif choice == 2:
            #by cell
            cell_index = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                       'input the cell index(x;y) of the matrix' + str(
                                                           self.curr_matrix[0])+'.split with ";"', 'OK',
                                                       'CANCEL', backgroundColor=(90, 90, 150),
                                                       promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            try:
                cell_index = [int(curr) for curr in cell_index.split(';')]
                if not 0 <= cell_index[0] <= len(self.curr_matrix[1][0]):
                    message_window.error('bad x index: expect between 0 and '+str(len(self.curr_matrix[1][0]))+'but got '+str(cell_index[0])+' instead')
                    return
                if not 0 <= cell_index[1] <= len(self.curr_matrix[1]):
                    message_window.error(
                    'bad y index: expect between 0 and ' + str(len(self.curr_matrix[1])) + 'but got ' + str(
                        cell_index[1]) + ' instead');return
                new_data = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                     'input the new data of the cell', 'OK',
                                                     'CANCEL', backgroundColor=(90, 90, 150),
                                                     promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                try:
                    new_data = float(new_data)
                    (self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)][1]) [cell_index[0]][cell_index[1]] = new_data
                    (self.all_matrix_dict[self.curr_matrix[0]]) [cell_index[0]][cell_index[1]] = new_data
                    self.curr_matrix[1] [cell_index[0]][cell_index[1]] = new_data
                except:message_window.error('bad input for float:'+str(new_data));return
            except Exception as e:
                message_window.error('failed to process because of the error:'+str(e))
                return
        elif choice == 3:
            #rename
            matrix_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200), 'input the name of the matrix', 'OK',
                                                      'CANCEL', backgroundColor=(90, 90, 150),
                                                      promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if matrix_name is None:
                message_window.warning(
                    'you did NOT select a name for the matrix!system will create a 10-length string randomly')
                matrix_name = random_string(10)
            if matrix_name.count('>') or matrix_name.count('|') or matrix_name.count(';'):
                message_window.error('you matrix name contains illegal chars:">","|" or ";"')
                return

            del self.all_matrix_dict[self.curr_matrix[0]]
            self.all_matrix_dict[matrix_name] = self.curr_matrix[1]
            self.all_matrix_data[self.all_matrix_data.index(self.curr_matrix)][0] = matrix_name
            self.curr_matrix[0] = matrix_name

        self.update = True

    def _cover_curr_preview(self):
        pygame.draw.rect(self.window, self.bkg_colour,
                         (0, 0, 1004, 150))
        pygame.draw.rect(self.window, self.bkg_colour,
                         (0, 150, 304, 460))
        #x:304~1004  y:150~610

    def copy_matrix(self):
        if self.curr_matrix is None:
            message_window.error('no matrix is selected')
            return
        matrix_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                  'input matrix name', 'OK',
                                                  'CANCEL', backgroundColor=(90, 90, 150),
                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        if matrix_name is not None:
            if '|' in matrix_name or '>' in matrix_name or ';' in matrix_name:
                message_window.warning(
                    "you matrix name includes '|', '>' or ';', which is(are) not allowed. system will create one randomly")
                matrix_name = random_string(5)
            if matrix_name in self.all_matrix_dict.keys():
                message_window.warning('the name of the matrix is included,system will add some random chars')
                new_name = (matrix_name + random_string(5))
                while new_name in self.all_matrix_dict.keys():
                    new_name = (matrix_name + random_string(5))
                matrix_name = new_name
            self.all_matrix_dict[matrix_name] = self.curr_matrix[1]
            self.all_matrix_data.append([matrix_name, self.curr_matrix[1]])

        self.curr_matrix_preview = WindowListViewer(self.curr_matrix[1], (700, 420), self.window, (304, 190))
        self.curr_matrix_title = self.curr_matrix[0]
        self.curr_matrix_preview_title = pygwidgets.TextButton(self.window, (304, 150), self.curr_matrix_title,
                                                               fontName='fonts/JetBrainsMono-Light.ttf',
                                                               width=700,
                                                               upColor=(135, 206, 250),
                                                               downColor=(135, 206, 250),
                                                               overColor=(135, 206, 250))
        self.update = True


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1004, 610))
    window.fill((0, 191, 255))
    #print(select_curr_matrix(window, [('a', [2, 3]), ('a', [2, 3])]))
    #a = subWindow(window, (0, 0), 1004, 610)
    #a.draw()
    k = ({}, [], None)
    while True:
        b = MatrixUi(window, clock, (0, 0), 1004, 610, all_data=k)
        k = b.draw()
    pygame.quit()
    sys.exit(0)

