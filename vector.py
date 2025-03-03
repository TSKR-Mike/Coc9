import random
import copy
import pygame,pygwidgets, pyghelpers
import math
from buttoncenter import ButtonCenter
import TableViewer
from EventPyghelpers import textYesNoDialogEventProgressing, textNumberDialogEventProgressing
from CoordinateSystem import CoordinateSystem3d
from TableViewer.Table import WindowListViewer
from checkbox import CheckBox
from statistics import Message_window
from matrix import subWindow
import pyperclip

message_window = Message_window()

"""
Notice:all the parameters have to be list of tuple.
"""
# 向量加法
def vector_add(u, v):
    return (ui + vi for ui, vi in zip(u, v))

# 向量减法
def vector_subtract(u, v):
    return (ui - vi for ui, vi in zip(u, v))

# 向量数乘
def scalar_multiply(k, u):
    return (k * ui for ui in u)

# 点积（内积）
def dot_product(u, v):
    return sum(ui * vi for ui, vi in zip(u, v))

# 向量长度（模）
def vector_length(u):
    return math.sqrt(sum(ui ** 2 for ui in u))

# 投影
def vector_projection(u, v):
    scale = dot_product(u, v) / dot_product(v, v)
    return scalar_multiply(scale, v)

# 向量夹角
def vector_angle(u, v):
    cos_theta = dot_product(u, v) / (vector_length(u) * vector_length(v))
    return math.acos(cos_theta)

# 向量标准化
def normalize_vector(u):
    length = vector_length(u)
    return (ui / length for ui in u)

# 向量叉积（2D 向量）
def cross_product_2d(u, v):
    if len(u) != 2 or len(v) != 2:
        raise ValueError("2D Cross product can only be used in 2D vectors")
    return u[0] * v[1] - u[1] * v[0]

# 向量反射
def vector_reflect(u, v):
    proj = vector_projection(u, v)
    return vector_subtract(u, scalar_multiply(2, proj))

# 向量叉积（3D 向量）
def cross_product_3d(u, v):
    if len(u) != 3 or len(v) != 3:
        raise ValueError("Cross product can only be used in 3D vectors")
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    )

# 向量点积（投影长度）
def projection_length(u, v):
    return dot_product(u, v) / vector_length(v)

def random_string(length:int):
    string = ''
    for _ in range(length):
        string += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return string

def load_vector_from_CocVectorInfo(file_name, names):
    if file_name.split('.')[-1] != 'CocVectorInfo':
        message_window.error('unsupported type:'+str(file_name.split('.')[-1])+';except type:CocVectorInfo')
        return
    with open(file_name, 'r') as matrix_file:
        try:
            all_complexes = []
            file_data = matrix_file.readlines()
            for curr in file_data:
                name, actual_data_str = curr.split('>')[0], curr.split('>')[1]
                if name in names:
                    name += random_string(2)
                    while name in names:
                        name = name[0:-1]
                        name += random_string(2)
                loaded_complex = actual_data_str
                all_complexes.append([name, loaded_complex])
            for curr in all_complexes:
                if '\n' in curr[1]:
                    curr[1] = curr[1][0:-1]
            return all_complexes
        except Exception as e:
            raise e

def write_vector_to_CocVectorInfo(file_name, vectors:list[(str, tuple)]):
    """
    :param vectors:
    :param file_name: str
    :return:
    """
    if len(vectors) == 0:return
    with open(file_name, 'w') as matrix_file:
        try:
            for vector in vectors:
                name = vector[0]
                matrix_file.write(str(name)+'>')
                data = str(vector[1])
                matrix_file.write(data+'\n')

        except Exception as e:
            raise e

def select_curr_vector(window, all_vectors, comments=''):
    if len(all_vectors) == 0:
        message_window.error('there is no available vector')
        return
    drawing_data = copy.deepcopy(all_vectors)
    drawing_data.insert(0, ['name', 'value'])
    for index in range(len(all_vectors) + 1):
        if index != 0:
            drawing_data[index].insert(0, str(index - 1))
        else:
            drawing_data[0].insert(0, '#')
    vector_selection = WindowListViewer(drawing_data, (1004, 304), window, (0, 190), auto_heading=False)
    select_by_index = textYesNoDialogEventProgressing(window, (0, 0, 1004, 190), 'How do you want to select the vector'+comments,
                                                     [vector_selection.draw], [vector_selection.handle_event], 'By index',
                                                     'By name', backgroundColor=(90, 90, 150))
    if select_by_index:
        vector_index = textNumberDialogEventProgressing(window, (0, 0, 1004, 190), 'input vector index '+comments,
                                                         [vector_selection.draw], [vector_selection.handle_event], 'OK',
                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                         promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0), allow_float=False, allow_negative=False)
        if vector_index is None:
            message_window.error('no inputs is given')
            return
        if 0 <= vector_index < len(all_vectors):
            return all_vectors[vector_index]
        else:
            message_window.error('Index out of range: get ' + str(vector_index) +' instead of a number between 0 and ' + str(len(all_vectors) - 1))
            return
    else:
        name = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                           'input the name of the vector', 'OK',
                                           'CANCEL', backgroundColor=(90, 90, 150),
                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        all_names = [curr[0] for curr in all_vectors]
        if name not in all_names:
            message_window.error('the name "'+name+'" is NOT included in all complexes')
            return
        for curr_complex in all_vectors:
            if curr_complex[0] == name:
                return curr_complex

def load_vector(window, clock, names, debug=False):
    loading_type_selector = CheckBox(2, ['input manually', 'load from .CocVectorInfo files'],
                                     1,
                                     window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30,
                                     buttons_adjust_length=0, background_color=(90, 90, 150))
    if loading_type_selector.clicked_choices == 'cancel':
        message_window.error('no inputs is given')
        return
    if len(loading_type_selector.clicked_choices) != 0:
        choice = loading_type_selector.clicked_choices[0]
        if choice == 0:
            # reset value
            x = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input the x value of the vector',[], [],
                                            'OK', 'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                            inputTextColor=(0, 0, 0))
            if x is None:
                message_window.error('no inputs is given.')
                return
            y = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input the y value of the vector',[],[], 'OK',
                                            'CANCEL', backgroundColor=(90, 90, 150),
                                            promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if y is None:
                message_window.error('no inputs is given.')
                return
            z = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input the z value of the vector',[], [], 'OK',
                                            'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if z is None:
                message_window.warning('no inputs for z is given. set as 0.')
                z = 0

            vector_name = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'input the name of the vectors', 'OK',
                                                      'CANCEL', backgroundColor=(90, 90, 150),
                                                      promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if vector_name is None:
                message_window.warning(
                    'you did NOT select a name for the vector!system will create a 10-length string randomly')
                vector_name = random_string(10)
            if vector_name.count('>'):
                message_window.error('you vector name contains illegal chars:">"')
                return
            if vector_name in names:
                message_window.warning('you name is the same as some in all complexes.system will add some random chars')
                vector_name += random_string(2)
                while vector_name in names:
                    vector_name = vector_name[0:len(vector_name) - 2]
                    vector_name += random_string(2)
            return [[vector_name, str(tuple([float(x), float(y), float(z)]))]]
        elif choice == 1:
            try:
                message_window.select_file(dir='VectorFiles')
                file_name = message_window.file_name
                return load_vector_from_CocVectorInfo(file_name, names)
            except Exception as e:
                if debug:
                    raise e
                return


class VectorUi(subWindow):

    def __init__(self, window, clock, loc, length, height, bkg_colour=(0, 191, 255), all_data=({}, [], None), no_mouse=False):
        super().__init__(window, loc, length, height, bkg_colour, 'Vector(You can interact with the chart by mouse[mid, left or scroll])')
        self.curr_vector_preview = None
        self.all_vector_preview = None
        self.clock = clock
        self.no_mouse = no_mouse
        self.all_vector_dict = all_data[0]
        # {<key:vector name>:(str),...}
        self.all_vector_data = all_data[1]
        # [[name, str], ...]
        self.curr_vector = all_data[2]
        # [name, str]
        self.all_buttons_line1 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 6,
                                              ['Select Vector', 'Vector Addition', 'Vector Subtract','Scalar Multiply', 'Dot Product', 'Vector Length'], self.window,
                                              150, 60, 0, 30, 152, 0, font='fonts/JetBrainsMono-Light.ttf',
                                              font_size=13,
                                              callbacks=None)
        self.all_buttons_line2 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 6,
                                              ['Extract Vector', 'Insert Vector', 'Clear selection', 'Modify Vector',
                                               'Copy Vector', 'Others'], self.window, 150, 60, 0, 90, 152, 0,
                                              font='fonts/JetBrainsMono-Light.ttf', font_size=13,
                                              callbacks=None)
        self.all_vector_preview_title = pygwidgets.TextButton(self.window, (0, 150), 'All complexes',
                                                              fontName='fonts/JetBrainsMono-Light.ttf', width=304,
                                                              upColor=(135, 206, 250), downColor=(135, 206, 250),
                                                              overColor=(135, 206, 250))

        self.curr_vector_title = 'No vector is selected'
        self.curr_vector_preview_title = pygwidgets.TextButton(self.window, (304, 150), self.curr_vector_title,
                                                               fontName='fonts/JetBrainsMono-Light.ttf', width=700,
                                                               upColor=(135, 206, 250), downColor=(135, 206, 250),
                                                               overColor=(135, 206, 250))

        self.update = False
        self.vectors_viewer = CoordinateSystem3d(self.window, (304, 190), (700, 420), 'All Vectors', no_mouse=self.no_mouse)
        if len(self.all_vector_data) != 0:
            for curr in self.all_vector_data:
                self.vectors_viewer.AddItem((0, 0, 0), turn_vector_str_to_tuple(curr[1]), label=curr[0])

    def draw(self):
        while True:
            # draw the bkground
            pygame.draw.rect(self.window, self.bkg_colour,
                             (self.loc[0], self.loc[1], self.length, self.height))  # draw the background
            pygame.draw.line(self.window, (135, 206, 250), (304, 150), (304, 610), width=3)  # draw the split line
            for curr in self.all_vector_data:
                if type(curr[1]) == tuple:
                    curr[1] = tuple([float(i) for i in list(curr[1])])
            # draw the view of all vectors
            if len(self.all_vector_data) != 0:
                if (type(self.all_vector_preview) != TableViewer.Table.WindowListViewer) or self.update:
                    drawing_data = copy.deepcopy(self.all_vector_data)
                    # 深拷贝，使drawing_data 与 all_complex_data 不会一起变化
                    # 如果直接赋值的话会一起变化 -> drawing_data = self.all_complex_data
                    # 需要注意!!!
                    drawing_data.insert(0, ['name', 'value'])
                    self.all_vector_preview = WindowListViewer(drawing_data, (304, 460), self.window, (0, 190),
                                                               auto_heading=False)
            else:
                self.all_vector_preview = pygwidgets.DisplayText(self.window, (70, 345), 'Nothing to show',
                                                                 fontName='fonts/JetBrainsMono-Light.ttf')

            self.vectors_viewer.draw()
            self.curr_vector_preview_title = pygwidgets.TextButton(self.window, (304, 150), self.curr_vector_title,
                                                                   fontName='fonts/JetBrainsMono-Light.ttf', width=700,
                                                                   upColor=(135, 206, 250), downColor=(135, 206, 250),
                                                                   overColor=(135, 206, 250))
            self.curr_vector_preview_title.draw()
            # draw others
            self.all_vector_preview_title.draw()
            self.all_vector_preview.draw()
            self.title_bkg.draw()
            self.title_view.draw()
            self.all_buttons_line1.drawAllButtons()
            self.all_buttons_line2.drawAllButtons()
            self.cancel_button.draw()
            self.minimize_button.draw()

            if self.update: self.update = False
            events = pygame.event.get()
            wheel_events, other = [], []
            for curr in events:
                if curr.type == pygame.MOUSEWHEEL:
                    wheel_events.append(curr)
                else:
                    other.append(curr)
            events = wheel_events + other
            for event in events:
                if type(self.curr_vector_preview) == TableViewer.Table.WindowListViewer: self.curr_vector_preview.handle_event(event)
                if type(self.all_vector_preview) == TableViewer.Table.WindowListViewer: self.all_vector_preview.handle_event(event)
                for curr in self.all_buttons_line1.Buttons:
                    if curr.handleEvent(event):
                        INDEX = self.all_buttons_line1.Buttons.index(curr)
                        if INDEX == 0:
                            # select vector
                            self.select_vector()
                        elif INDEX == 1:
                            # addition
                            self.addition()
                        elif INDEX == 2:
                            # subtraction
                            self.subtraction()
                        elif INDEX == 3:
                            # Scalar Multiply
                            self.scalar_multiply()
                        elif INDEX == 4:
                            # Dot Product
                            self.dot_product()
                        elif INDEX == 5:
                            # Vector Length
                            self.length()

                for curr in self.all_buttons_line2.Buttons:
                    if curr.handleEvent(event):
                        INDEX = self.all_buttons_line2.Buttons.index(curr)
                        if INDEX == 0:
                            # extract vector
                            self.extract_vector()
                        elif INDEX == 1:
                            # insert vector
                            self.insert_vector()
                        elif INDEX == 2:
                            # clear current vector
                            self.clear_curr_vector()
                        elif INDEX == 3:
                            # change vector
                            self.change_curr_vector()
                        elif INDEX == 4:
                            # copy vector
                            self.copy_vector()
                        elif INDEX == 5:
                            # others
                            self.others()
                if self.cancel_button.handleEvent(event):
                    if message_window.question(
                            question='If leave now, all you data WILL NOT BE SAVED. Do you want to save them?'):
                        self.extract_vector()
                    return {}, [], None
                if self.minimize_button.handleEvent(event):
                    return self.all_vector_dict, self.all_vector_data, self.curr_vector
                self.vectors_viewer.handle_event(event)
            pygame.display.update()

    def load_matrix(self):
        all_complexes = load_vector(self.window, self.clock, [i[0] for i in self.all_vector_data])
        if all_complexes is not None:
            for curr in all_complexes:
                name = curr[0]
                data = curr[1]
                self.all_vector_dict[str(name)] = data
                c = turn_vector_str_to_tuple(data)
                data = tuple([float(i) for i in data])
                self.all_vector_data.append([name, data])
                self.vectors_viewer.AddItem((0, 0, 0), c, label=name)
            self.update = True

    def remove_matrix(self, matrix_name: str):
        if matrix_name not in self.all_vector_dict.keys():
            message_window.error('the vector "' + matrix_name + '" does not exist')
        else:
            del self.all_vector_dict[matrix_name]
            index = 0
            for i in self.all_vector_data:
                if str(i[0]) == matrix_name:
                    del self.all_vector_data[index]
                    return
                index += 1
            self.update = True

    def extract_vector(self):
        file_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                'input file name(will be saved in "/MatrixFiles" dir)', 'OK',
                                                'CANCEL', backgroundColor=(90, 90, 150),
                                                promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        file_name = str(file_name)
        write_vector_to_CocVectorInfo("VectorFiles/" + file_name + '.CocVectorInfo', self.all_vector_data)
        message_window.message('extract completed')

    def select_vector(self, fresh_curr_complex=True, comments=''):
        m = select_curr_vector(self.window, self.all_vector_data, comments)
        if m is None: return
        self.update = True
        if fresh_curr_complex:
            self.curr_vector = m
            self.curr_vector_title = 'Curr vector:' + m[0]
        else:
            return m

    def insert_vector(self):
        all_complexes = load_vector(self.window, self.clock, [i[0] for i in self.all_vector_data])
        if all_complexes is None or len(all_complexes) == 0:
            return
        for curr_complex in all_complexes:
            self.all_vector_dict[curr_complex[0]] = curr_complex[1]
            self.all_vector_data.append(list(curr_complex))
            c = turn_vector_str_to_tuple(curr_complex[1])
            self.vectors_viewer.AddItem((0, 0, 0), c, label=curr_complex[0])
        message_window.message('insert completed')
        self.update = True

    def clear_curr_vector(self):
        self.curr_vector = None;self.update = True;self.curr_vector_title = 'No vector is selected'

    def addition(self):
        if self.curr_vector is None:
            self.select_vector(comments=' for addition(1)')
        other = self.select_vector(fresh_curr_complex=False, comments=' for addition(2)')
        quit = False
        if self.curr_vector is None:
            message_window.error('the first vector of the addition did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second vector of addiction did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                       'input vector name for the result', 'OK',
                                                       'CANCEL', backgroundColor=(90, 90, 150),
                                                       promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if complex_name is not None:
                if '>' in complex_name:
                    message_window.warning(
                        "you vector name includes '>', which is not allowed. system will create one randomly")
                    complex_name = random_string(5)
                if complex_name in self.all_vector_dict.keys():
                    message_window.warning('the name of the vector is included,system will add some random chars')
                    new_name = (complex_name + random_string(5))
                    while new_name in self.all_vector_dict.keys():
                        new_name = (complex_name + random_string(5))
                    complex_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one randomly')
                complex_name = random_string(7)
                while complex_name in self.all_vector_dict.keys():
                    complex_name = random_string(7)
            try:
                answer = vector_add(turn_vector_str_to_tuple(self.curr_vector[1]), turn_vector_str_to_tuple(other[1]))
                answer = str(answer)
                self.all_vector_data.append([complex_name, answer])
                self.all_vector_dict[complex_name] = answer
                c = turn_vector_str_to_tuple(answer)
                self.vectors_viewer.AddItem((0, 0, 0), c, label=complex_name)
                self.update = True
            except Exception as e:
                message_window.error('can not add the two complexes because of the error:' + str(e))
                return

    def subtraction(self):
        if self.curr_vector is None:
            self.select_vector(comments=' for subtraction(1)')
        other = self.select_vector(fresh_curr_complex=False, comments=' for subtraction(2)')
        quit = False
        if self.curr_vector is None:
            message_window.error('the first vector of the subtraction did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second vector of subtraction did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                       'input vector name for the result', 'OK',
                                                       'CANCEL', backgroundColor=(90, 90, 150),
                                                       promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if complex_name is not None:
                if '>' in complex_name:
                    message_window.warning(
                        "you vector name includes '>', which is not allowed. system will create one randomly")
                    complex_name = random_string(5)
                if complex_name in self.all_vector_dict.keys():
                    message_window.warning('the name of the vector is included,system will add some random chars')
                    new_name = (complex_name + random_string(5))
                    while new_name in self.all_vector_dict.keys():
                        new_name = (complex_name + random_string(5))
                    complex_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one randomly')
                complex_name = random_string(7)
                while complex_name in self.all_vector_dict.keys():
                    complex_name = random_string(7)
            try:
                answer = vector_subtract(turn_vector_str_to_tuple(self.curr_vector[1]), turn_vector_str_to_tuple(other[1]))
                answer = str(answer)
                self.all_vector_data.append([complex_name, answer])
                self.all_vector_dict[complex_name] = answer
                c = turn_vector_str_to_tuple(answer)
                self.vectors_viewer.AddItem((0, 0, 0), c, label=complex_name)
                self.update = True
            except Exception as e:
                message_window.error('can not add the two complexes because of the error:' + str(e))
                return

    def change_curr_vector(self):
        if self.curr_vector is None:
            message_window.error('no vector is selected!')
            return
        changing_type_selector = CheckBox(2,
                                          ['reset value', 'RENAME'],
                                          1,
                                          self.window, self.clock, first_x=60, first_y=100, each_add_x=0, each_add_y=30,
                                          buttons_adjust_length=0, background_color=(90, 90, 150))
        if len(changing_type_selector.clicked_choices) == 0 or type(
            changing_type_selector.clicked_choices) == str: return
        choice = changing_type_selector.clicked_choices[0]

        if choice == 0:
            # reset value
            x = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200), 'input the x value of the vector',
                                               'OK',
                                               'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                               inputTextColor=(0, 0, 0))
            if x is None:
                message_window.error('no inputs is given.')
                return
            try:
                float(x)
            except:
                message_window.error('bad input for float:' + str(x))
                return
            y = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                  'input the y value of the vector', 'OK',
                                                  'CANCEL', backgroundColor=(90, 90, 150),
                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if y is None:
                message_window.error('no inputs is given.')
                return
            try:
                float(y)
            except:
                message_window.error('bad input for float:' + str(y))
                return
            z = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                            'input the z value of the vector', 'OK',
                                            'CANCEL', backgroundColor=(90, 90, 150),
                                            promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if z is None:
                message_window.warning('no inputs for z is given. set as 0.')
                z = '0'
            try:
                float(z)
            except:
                message_window.error('bad input for float:' + str(z))
                return

            self.all_vector_data[self.all_vector_data.index(self.curr_vector)][1] = str(tuple([x, y, z]))
            self.curr_vector[1] = str(tuple([x, y, z]))
            self.all_vector_dict[self.curr_vector[0]] = str(tuple([x, y, z]))
        elif choice == 1:
            # rename
            name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                               'input the name of the vector', 'OK',
                                               'CANCEL', backgroundColor=(90, 90, 150),
                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if name is None:
                message_window.error('no inputs is given')
                return
            if name in self.all_vector_dict.keys():
                message_window.warning('the name is the same as others.system will add some random chars.')
                name += random_string(2)
                while name in self.all_vector_dict.keys():
                    name = name[0:len(name) - 2]
                    name += random_string(2)
            del self.all_vector_dict[self.curr_vector[0]]
            self.all_vector_dict[name] = self.curr_vector[1]
            self.all_vector_data[self.all_vector_data.index(self.curr_vector)][0] = name
            self.curr_vector[0] = name
        self.update = True

    def copy_vector(self):
        if self.curr_vector is None:
            message_window.error('no vector is selected')
            return
        vector_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                   'input vector name for the result', 'OK',
                                                   'CANCEL', backgroundColor=(90, 90, 150),
                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        if vector_name is not None:
            if '|' in vector_name or '>' in vector_name or ';' in vector_name:
                message_window.warning(
                    "you vector name includes '|', '>' or ';', which is(are) not allowed. system will create one randomly")
                vector_name = random_string(5)
            if vector_name in self.all_vector_dict.keys():
                message_window.warning('the name of the vector is included,system will add some random chars')
                new_name = (vector_name + random_string(5))
                while new_name in self.all_vector_dict.keys():
                    new_name = (vector_name + random_string(5))
                vector_name = new_name
            self.all_vector_dict[vector_name] = self.curr_vector[1]
            self.all_vector_data.append([vector_name, self.curr_vector[1]])
            c = turn_vector_str_to_tuple(self.curr_vector[1])
            self.vectors_viewer.AddItem((0, 0, 0), c, label=vector_name)

        self.curr_vector_preview = WindowListViewer(self.curr_vector[1], (700, 420), self.window, (304, 190))
        self.curr_vector_title = self.curr_vector[0]
        self.curr_vector_preview_title = pygwidgets.TextButton(self.window, (304, 150), self.curr_vector_title,
                                                                fontName='fonts/JetBrainsMono-Light.ttf',
                                                                width=700,
                                                                upColor=(135, 206, 250),
                                                                downColor=(135, 206, 250),
                                                                overColor=(135, 206, 250))
        self.update = True

    def scalar_multiply(self):
        if self.curr_vector is None:
            self.select_vector(comments='for subtraction(1)')
        other = self.select_vector(fresh_curr_complex=False, comments='for subtraction(2)')
        quit = False
        if self.curr_vector is None:
            message_window.error('the first vector of the subtraction did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second vector of subtraction did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                       'input vector name for the result', 'OK',
                                                       'CANCEL', backgroundColor=(90, 90, 150),
                                                       promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if complex_name is not None:
                if '>' in complex_name:
                    message_window.warning(
                        "you vector name includes '>', which is not allowed. system will create one randomly")
                    complex_name = random_string(5)
                if complex_name in self.all_vector_dict.keys():
                    message_window.warning('the name of the vector is included,system will add some random chars')
                    new_name = (complex_name + random_string(5))
                    while new_name in self.all_vector_dict.keys():
                        new_name = (complex_name + random_string(5))
                    complex_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one randomly')
                complex_name = random_string(5)
                while complex_name in self.all_vector_dict.keys():
                    complex_name = random_string(5)
            try:
                answer = scalar_multiply(turn_vector_str_to_tuple(self.curr_vector[1]), turn_vector_str_to_tuple(other[1]))
                answer = str(answer)
                self.all_vector_data.append([complex_name, answer])
                self.all_vector_dict[complex_name] = answer
                c = turn_vector_str_to_tuple(answer)
                self.vectors_viewer.AddItem((0, 0, 0), c, label=complex_name)
                self.update = True
            except Exception as e:
                message_window.error('can not add the two complexes because of the error:' + str(e))
                return

    def dot_product(self):
        if self.curr_vector is None:
            self.select_vector(comments=' for subtraction(1)')
        other = self.select_vector(fresh_curr_complex=False, comments=' for subtraction(2)')
        quit = False
        if self.curr_vector is None:
            message_window.error('the first vector of the subtraction did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second vector of subtraction did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                       'input vector name for the result', 'OK',
                                                       'CANCEL', backgroundColor=(90, 90, 150),
                                                       promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if complex_name is not None:
                if '>' in complex_name:
                    message_window.warning(
                        "you vector name includes '>', which is not allowed. system will create one randomly")
                    complex_name = random_string(5)
                if complex_name in self.all_vector_dict.keys():
                    message_window.warning('the name of the vector is included,system will add some random chars')
                    new_name = (complex_name + random_string(5))
                    while new_name in self.all_vector_dict.keys():
                        new_name = (complex_name + random_string(5))
                    complex_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one randomly')
                complex_name = random_string(7)
                while complex_name in self.all_vector_dict.keys():
                    complex_name = random_string(7)
            try:
                answer = dot_product(turn_vector_str_to_tuple(self.curr_vector[1]), turn_vector_str_to_tuple(other[1]))
                answer = str(answer)
                self.all_vector_data.append([complex_name, answer])
                self.all_vector_dict[complex_name] = answer
                c = turn_vector_str_to_tuple(answer)
                self.vectors_viewer.AddItem((0, 0, 0), c, label=complex_name)
                self.update = True
            except Exception as e:
                message_window.error('can not add the two complexes because of the error:' + str(e))
                return

    def others(self):
        type_selector = CheckBox(6,
                                 ['Remove Curr Vec','Vector Projection', 'Vector Angle', 'Normalize Vector', 'Cross Product',
                                  'Projection Length'],
                                 1,
                                 self.window, self.clock, first_x=40, first_y=50, each_add_x=0, each_add_y=30,
                                 buttons_adjust_length=0, background_color=(90, 90, 150))
        if type_selector.clicked_choices == 'cancel' or len(type_selector.clicked_choices) == 0:
            message_window.error('no choice is selected')
            return
        choice = type_selector.clicked_choices[0]
        self.update = True
        if choice == 0:
            if self.curr_vector is None:
                message_window.error('no current vector is selected!')
                self.select_vector()
                return
            del self.all_vector_data[self.all_vector_data.index(self.curr_vector)]
            del self.all_vector_dict[self.curr_vector[0]]
            self.curr_vector = None
            self.update = True
        else:
            if choice != 3:
                if self.curr_vector is None:
                    message_window.error('no current vector is selected!')
                    self.select_vector()
                    return
                other = self.select_vector(fresh_curr_complex=False, comments=' for '+['Remove Curr Vec','Vector Projection', 'Vector Angle', 'Normalize Vector', 'Cross Product',
                                  'Projection Length'][choice])
                if other is None:
                    message_window.error('the second vector did NOT select correctly')
                    return
                vector_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                           'input vector name for the result for ' + ['Remove Curr Vec','Vector Projection', 'Vector Angle', 'Normalize Vector', 'Cross Product',
                                                            'Projection Length'][choice], 'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                if vector_name is not None:
                    if '>' in vector_name:
                        message_window.warning(
                            "you vector name includes '>', which is not allowed. system will create one randomly")
                        vector_name = random_string(5)
                    if vector_name in self.all_vector_dict.keys():
                        message_window.warning('the name of the vector is included,system will add some random chars')
                        new_name = (vector_name + random_string(5))
                        while new_name in self.all_vector_dict.keys():
                            new_name = (vector_name + random_string(5))
                        vector_name = new_name
                u = turn_vector_str_to_tuple(self.curr_vector[1])
                v = turn_vector_str_to_tuple(other[1])
                if choice == 1:
                    answer = vector_projection(u, v)
                elif choice == 2:
                    answer = vector_angle(u, v)
                elif choice == 4:
                    answer = cross_product_3d(u, v)
                elif choice == 5:
                    answer = projection_length(u, v)
                    copy_answer = pyghelpers.textYesNoDialog(self.window, (0, 0, 1004, 300),
                                                             'The projection length is:' + str(answer),
                                                             'copy', "cancel")
                    if copy_answer:
                        pyperclip.copy(str(answer))
                    return
                else:return
                self.all_vector_data.append([vector_name, str(answer)])
                self.all_vector_dict[vector_name] = str(answer)
            else:
                if choice == 3:
                    if self.curr_vector is None:
                        message_window.error('no current vector is selected!')
                        self.select_vector()
                        return
                    vector_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                              'input vector name for the result for Normalize Vector', 'OK', 'CANCEL',
                                                              backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                    if vector_name is not None:
                        if '>' in vector_name:
                            message_window.warning(
                                "you vector name includes '>', which is not allowed. system will create one randomly")
                            vector_name = random_string(5)
                        if vector_name in self.all_vector_dict.keys():
                            message_window.warning('the name of the vector is included,system will add some random chars')
                            new_name = (vector_name + random_string(5))
                            while new_name in self.all_vector_dict.keys():
                                new_name = (vector_name + random_string(5))
                            vector_name = new_name
                    u = turn_vector_str_to_tuple(self.curr_vector[1])
                    answer = normalize_vector(u)
                    self.all_vector_data.append([vector_name, str(answer)])
                    self.all_vector_dict[vector_name] = str(answer)

    def length(self):
        if self.curr_vector is None:
            message_window.error('no current vector is selected')
            self.select_vector()
            return
        length = math.sqrt(sum([cu**2 for cu in turn_vector_str_to_tuple(self.curr_vector[1])]))
        copy_answer = pyghelpers.textYesNoDialog(self.window, (0, 0, 1004, 300),
                                                 'The length is:' + str(length),
                                                 'copy', "cancel")
        if copy_answer:
            pyperclip.copy(str(length))


def turn_vector_str_to_tuple(string:str):
    """
    :param string: in forms like '(1, 2, 3)'
    :return: tuple, like(1.0, 2.0)
    """
    if ('[' in string and ']' in string) or ('(' in string and ')' in string):
        result = string[1:-1]
    else:
        result = string
    result = result.split(',')
    result = [float(i.strip()) for i in result]
    return tuple(result)

# 测试
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1004, 610))
    window.fill((0, 191, 255))
    k = ({}, [], None)
    while True:
        b = VectorUi(window, clock, (0, 0), 1004, 610, all_data=k)
        k = b.draw()
    pygame.quit()
    sys.exit(0)
