import random
import sys
import copy
import pygame, pygwidgets, pyghelpers
from pyghelpers import textYesNoDialog
import math
from buttoncenter import ButtonCenter
import TableViewer
from EventPyghelpers import textAnswerDialogEventProgressing, textYesNoDialogEventProgressing, textNumberDialogEventProgressing
from CoordinateSystem import CoordinateSystem2d, ARROW
from TableViewer.Table import WindowListViewer
import numpy as np
from checkbox import CheckBox
from statistics import Message_window
import cmath
from matrix import subWindow
import pyperclip

message_window = Message_window()

def random_string(length:int):
    string = ''
    for _ in range(length):
        string += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return string

def ComplexAddition(complex1:complex, complex2:complex):
    return complex1 + complex2

def ComplexMultiplication(complex1:complex, complex2:complex):
    return complex1 * complex2

def ComplexDivision(complex1:complex, complex2:complex):
    return complex1 / complex2

def ComplexSubtraction(complex1:complex, complex2:complex):
    return complex1 - complex2

def ComplexConjugate(complex1:complex):
    return complex1.conjugate()

def ComplexAbs(complex1:complex):
    return abs(complex1)

def ComplexAngle(complex1:complex):
    return complex1.real / abs(complex1)

def ComplexToPolar(complex1:complex):
    return cmath.polar(complex1)

def load_complex_from_CocComplexInfo(file_name, names):
    if file_name.split('.')[-1] != 'CocComplexInfo':
        message_window.error('unsupported type:'+str(file_name.split('.')[-1])+';except type:CocComplexInfo')
        return
    with open(file_name, 'r') as matrix_file:
        try:
            all_complexes = []
            file_data = matrix_file.readlines()
            for curr in file_data:
                name, actual_data_str = curr.split('>')[0], curr.split('>')[1]
                loaded_complex = actual_data_str
                all_complexes.append([name, loaded_complex])
            for curr in all_complexes:
                if '\n' in curr[1]:
                    curr[1] = curr[1][0:-1]
            return all_complexes
        except Exception as e:
            raise e

def write_complex_to_CocComplexInfo(file_name, complexes:list[(str,complex)]):
    """
    :param complexes:
    :param file_name: str
    :return:
    """
    if len(complexes) == 0:return
    with open(file_name, 'w') as matrix_file:
        try:
            for complex in complexes:
                name = complex[0]
                matrix_file.write(str(name)+'>')
                data = str(complex[1])
                matrix_file.write(data+'\n')

        except Exception as e:
            raise e

def select_curr_complex(window, all_complexes, comments=''):
    if len(all_complexes) == 0:
        message_window.error('there is no available complex')
        return
    drawing_data = copy.deepcopy(all_complexes)
    drawing_data.insert(0, ['name', 'value'])
    for index in range(len(all_complexes) + 1):
        if index != 0:
            drawing_data[index].insert(0, str(index - 1))
        else:
            drawing_data[0].insert(0, '#')
    complex_selection = WindowListViewer(drawing_data, (1004, 304), window, (0, 190), auto_heading=False)
    select_by_index = textYesNoDialogEventProgressing(window, (0, 0, 1004, 190), 'How do you want to select the complex'+comments,
                                                     [complex_selection.draw], [complex_selection.handle_event], 'By index',
                                                     'By name', backgroundColor=(90, 90, 150))
    if select_by_index:
        complex_index = textAnswerDialogEventProgressing(window, (0, 0, 1004, 190), 'input complex index '+comments,
                                                         [complex_selection.draw], [complex_selection.handle_event], 'OK',
                                                         'CANCEL', backgroundColor=(90, 90, 150),
                                                         promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        if complex_index is None:
            message_window.error('exit because of empty input')
            return
        try:
            complex_index = int(complex_index)
        except:
            message_window.error('bad inputs for int:"'+str(complex_index)+'"')
            return
        if 0 <= complex_index < len(all_complexes):
            return all_complexes[complex_index]
        else:
            message_window.error('Index out of range: get ' + str(complex_index) +' instead of a number between 0 and ' + str(len(all_complexes) - 1))
            return
    else:
        name = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                           'input the name of the complex', 'OK',
                                           'CANCEL', backgroundColor=(90, 90, 150),
                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        all_names = [curr[0] for curr in all_complexes]
        if name not in all_names:
            message_window.error('the name "'+name+'" is NOT included in all complexes')
            return
        for curr_complex in all_complexes:
            if curr_complex[0] == name:
                return curr_complex

def load_complex(window, clock, names, debug=False):
    loading_type_selector = CheckBox(2, ['input manually', 'load from .CocComplexInfo files'],
                                     1,
                                     window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30,
                                     buttons_adjust_length=0, background_color=(90, 90, 150))
    if loading_type_selector.clicked_choices == 'cancel':
        message_window.error('no inputs is given')
        return
    if len(loading_type_selector.clicked_choices) != 0:
        choice = loading_type_selector.clicked_choices[0]
        if choice == 0:
            real = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input the real part of the complex',
                                               [], [], 'OK', 'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                               inputTextColor=(0, 0, 0))
            if real is None:
                message_window.error('no inputs is given.')
                return
            imagine = textNumberDialogEventProgressing(window, (0, 0, 1004, 200), 'input the imaginary value(do NOT contain "j)" of the complex',[], [], 'OK',
                                                  'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if imagine is None:
                message_window.error('no inputs is given.')
                return
            complex_name = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'input the name of the complexes', 'OK',
                                                      'CANCEL', backgroundColor=(90, 90, 150),
                                                      promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if complex_name is None:
                message_window.warning(
                    'you did NOT select a name for the complex!system will create a 10-length string randomly')
                complex_name = random_string(10)
            if complex_name.count('>'):
                message_window.error('you complex name contains illegal chars:">"')
                return
            if complex_name in names:
                message_window.warning('you name is the same as some in all complexes.system will add some random chars')
                complex_name += random_string(2)
                while complex_name in names:
                    complex_name = complex_name[0:len(complex_name) - 2]
                    complex_name += random_string(2)
            return [[complex_name, str(complex(str(real)+'+'+str(imagine)+'j'))]]
        elif choice == 1:
            try:
                message_window.select_file(dir='ComplexFiles')
                file_name = message_window.file_name
                return load_complex_from_CocComplexInfo(file_name, names)
            except Exception as e:
                if debug:
                    raise e
                return

def all_complex_square_roots(z):
    r = abs(z)  # 模
    theta = cmath.phase(z)  # 幅角
    sqrt_r = math.sqrt(r)
    root1 = cmath.rect(sqrt_r, theta / 2)  # 第一个平方根
    root2 = cmath.rect(sqrt_r, (theta + 2 * math.pi) / 2)  # 第二个平方根
    return root1, root2

def all_complex_cube_roots(z):
    r = abs(z)  # 模
    theta = cmath.phase(z)  # 幅角
    cube_r = r ** (1/3)  # 模的立方根
    roots = []
    for k in range(3):
        angle = (theta + 2 * k * math.pi) / 3
        root = cmath.rect(cube_r, angle)
        roots.append(root)
    return roots

class ComplexUi(subWindow):


    def __init__(self, window, clock, loc, length, height, bkg_colour=(0, 191, 255), all_data=({}, [], None), no_mouse=False):
        super().__init__(window, loc, length, height, bkg_colour, 'Complex(You can drag the chart to interact with it)')
        self.curr_complex_preview = None
        self.all_complex_preview = None
        self.clock = clock
        self.all_complex_dict = all_data[0]
        self.no_mouse = no_mouse
        # {<key:complex name>:(str),...}
        self.all_complex_data = all_data[1]
        # [[name, str], ...]
        self.curr_complex = all_data[2]
        #[name, str]
        self.all_buttons_line1 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 6,
                     ['Select Complex', 'Complex Addition', 'Complex Subtract', 'Multiplication', 'Complex Division', 'Complex Conjugate'], self.window, 150, 60, 0, 30, 152, 0, font='fonts/JetBrainsMono-Light.ttf', font_size=13,
                     callbacks=None)
        self.all_buttons_line2 = ButtonCenter(None, (0, 0, 0), (90, 90, 150), (0, 50, 100), (20, 0, 80), 6,
                                              ['Extract Complex', 'Insert Complex', 'Clear selection', 'Modify Complex', 'Copy Complex', 'Others'], self.window, 150, 60, 0, 90, 152, 0,
                                              font='fonts/JetBrainsMono-Light.ttf', font_size=13,
                                              callbacks=None)
        self.all_complex_preview_title = pygwidgets.TextButton(self.window, (0, 150), 'All complexes', fontName='fonts/JetBrainsMono-Light.ttf', width=304,
                                                               upColor=(135, 206, 250), downColor=(135, 206, 250), overColor=(135, 206, 250))

        self.curr_matrix_title = 'No complex is selected'
        self.curr_matrix_preview_title = pygwidgets.TextButton(self.window, (304, 150), self.curr_matrix_title,
                                                               fontName='fonts/JetBrainsMono-Light.ttf', width=700,
                                                               upColor=(135, 206, 250), downColor=(135, 206, 250),
                                                               overColor=(135, 206, 250))

        self.update = False
        self.complexes_viewer = CoordinateSystem2d(self.window, (304, 190), (700, 420), 'all complexes', 'x', 'i', no_mouse=self.no_mouse)
        if len(self.all_complex_data) != 0:
            for curr in self.all_complex_data:
                self.complexes_viewer.AddItem((0, 0), turn_complex_str_to_tuple(curr[1]), label=curr[0])

    def draw(self):
        while True:
            #draw the bkground
            pygame.draw.rect(self.window, self.bkg_colour, (self.loc[0], self.loc[1], self.length, self.height))# draw the background
            pygame.draw.line(self.window, (135, 206, 250), (304, 150), (304, 610), width=3)# draw the split line
            #draw the view of all complexes:num->2
            self.all_complex_data = [list(i) for i in self.all_complex_data]
            if len(self.all_complex_data) != 0:
                if (type(self.all_complex_preview) != TableViewer.Table.WindowListViewer) or self.update:
                    drawing_data = copy.deepcopy(self.all_complex_data)
                    #深拷贝，使drawing_data 与 all_complex_data 不会一起变化
                    #如果直接赋值的话会一起变化 -> drawing_data = self.all_complex_data
                    #需要注意!!!
                    drawing_data.insert(0, ['name', 'value'])
                    self.all_complex_preview = WindowListViewer(drawing_data, (304, 460), self.window, (0, 190), auto_heading=False)
            else:
                self.all_complex_preview = pygwidgets.DisplayText(self.window, (70, 345), 'Nothing to show', fontName='fonts/JetBrainsMono-Light.ttf')

            if self.update:
                self.complexes_viewer = CoordinateSystem2d(self.window, (304, 190), (700, 420), 'all complexes', 'x',
                                                           'i', no_mouse=self.no_mouse)
                for curr in self.all_complex_data:
                    self.complexes_viewer.AddItem((0, 0), turn_complex_str_to_tuple(curr[1]), label=curr[0])

            self.complexes_viewer.draw()
            self.curr_matrix_preview_title = pygwidgets.TextButton(self.window, (304, 150), self.curr_matrix_title,
                                                                   fontName='fonts/JetBrainsMono-Light.ttf', width=700,
                                                                   upColor=(135, 206, 250), downColor=(135, 206, 250),
                                                                   overColor=(135, 206, 250))
            self.curr_matrix_preview_title.draw()
            #draw others
            self.all_complex_preview_title.draw()
            self.all_complex_preview.draw()
            self.title_bkg.draw()
            self.title_view.draw()
            self.all_buttons_line1.drawAllButtons()
            self.all_buttons_line2.drawAllButtons()
            self.cancel_button.draw()
            self.minimize_button.draw()

            if self.update:self.update = False
            for event in pygame.event.get():
                if type(self.curr_complex_preview) == TableViewer.Table.WindowListViewer:self.curr_complex_preview.handle_event(event)
                if type(self.all_complex_preview) == TableViewer.Table.WindowListViewer:self.all_complex_preview.handle_event(event)
                for curr in self.all_buttons_line1.Buttons:
                    if curr.handleEvent(event):
                        INDEX = self.all_buttons_line1.Buttons.index(curr)
                        if INDEX == 0:
                            #select complex
                            self.select_complex()
                        elif INDEX == 1:
                            #addition
                            self.addition()
                        elif INDEX == 2:
                            #subtraction
                            self.subtraction()
                        elif INDEX ==3:
                            #multiplication
                            self.multiplication()
                        elif INDEX == 4:
                            #division
                            self.division()
                        elif INDEX == 5:
                            #conjugate
                            self.conjugate()

                for curr in self.all_buttons_line2.Buttons:
                    if curr.handleEvent(event):
                        INDEX = self.all_buttons_line2.Buttons.index(curr)
                        if INDEX == 0:
                            #extract complex
                            self.extract_complex()
                        elif INDEX == 1:
                            #insert complex
                            self.insert_complex()
                        elif INDEX == 2:
                            #clear current complex
                            self.clear_curr_complex()
                        elif INDEX == 3:
                            #change complex
                            self.change_curr_complex()
                        elif INDEX == 4:
                            #copy complex
                            self.copy_complex()
                        elif INDEX == 5:
                            #others
                            self.others()
                if self.cancel_button.handleEvent(event):
                    if message_window.question(question='If leave now, all you data WILL NOT BE SAVED. Do you want to save them?'):
                        self.extract_complex()
                    return {}, [], None

                if self.minimize_button.handleEvent(event):
                    return self.all_complex_dict,self.all_complex_data,self.curr_complex

                self.complexes_viewer.handle_event(event)
            pygame.display.update()

    def load_matrix(self):
        all_complexes = load_complex(self.window, self.clock, [i[0] for i in self.all_complex_data])
        if all_complexes is not None:
            for curr in all_complexes:
                name = curr[0]
                data = curr[1]
                self.all_complex_dict[str(name)] = data
                c = turn_complex_str_to_tuple(data)
                self.all_complex_data.append([name, data])
                self.complexes_viewer.AddItem((0,0), c, label=name)
            self.update = True

    def remove_matrix(self, matrix_name:str):
        if matrix_name not in self.all_complex_dict.keys():
            message_window.error('the complex "'+matrix_name+'" does not exist')
        else:
            del self.all_complex_dict[matrix_name]
            index = 0
            for i in self.all_complex_data:
                if str(i[0]) == matrix_name:
                    del self.all_complex_data[index]
                    return
                index += 1
            self.update = True

    def extract_complex(self):
        file_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200), 'input file name(will be saved in "/MatrixFiles" dir)', 'OK',
                                                        'CANCEL', backgroundColor=(90, 90, 150),
                                                        promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        file_name = str(file_name)
        write_complex_to_CocComplexInfo("ComplexFiles/" + file_name +'.CocComplexInfo', self.all_complex_data)
        message_window.message('extract completed')

    def select_complex(self, fresh_curr_complex=True, comments=''):
        m = select_curr_complex(self.window, self.all_complex_data, comments)
        if m is None:return
        self.update = True
        if fresh_curr_complex:
            self.curr_complex = m
            self.curr_matrix_title = 'Curr complex:'+m[0]
        else:
            return m

    def insert_complex(self):
        all_complexes = load_complex(self.window, self.clock, [i[0] for i in self.all_complex_data])
        if all_complexes is None or len(all_complexes) == 0:
            return
        for name, value in all_complexes:
            if name in self.all_complex_dict.keys():
                name += random_string(2)
                while name in self.all_complex_dict.keys():
                    name = name[0:-1]
                    name += random_string(2)
        for curr_complex in all_complexes:
            self.all_complex_dict[curr_complex[0]] = curr_complex[1]
            self.all_complex_data.append(curr_complex)
            print(curr_complex)
            c = turn_complex_str_to_tuple(curr_complex[1])
            self.complexes_viewer.AddItem((0,0), c, label=curr_complex[0])
        message_window.message('insert completed')
        self.update = True

    def clear_curr_complex(self):self.curr_complex = None;self.update = True;self.curr_matrix_title='No complex is selected'

    def addition(self):
        if self.curr_complex is None:
            self.select_complex(comments='for addition(1)')
        other = self.select_complex(fresh_curr_complex=False, comments='for addition(2)')
        quit = False
        if self.curr_complex is None:
            message_window.error('the first complex of the addition did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second complex of addiction did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                    'input complex name for the result', 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if complex_name is not None:
                if '>' in complex_name:
                    message_window.warning("you complex name includes '>', which is not allowed. system will create one randomly")
                    complex_name = random_string(5)
                if complex_name in self.all_complex_dict.keys():
                    message_window.warning('the name of the complex is included,system will add some random chars')
                    new_name = (complex_name + random_string(5))
                    while new_name in self.all_complex_dict.keys():
                        new_name = (complex_name + random_string(5))
                    complex_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one randomly')
                complex_name = random_string(7)
                while complex_name in self.all_complex_dict.keys():
                    complex_name = random_string(7)
            try:
                answer = ComplexAddition(complex(self.curr_complex[1]), complex(other[1]))
                answer = str(answer)
                self.all_complex_data.append((complex_name, answer))
                self.all_complex_dict[complex_name] = answer
                c = turn_complex_str_to_tuple(answer)
                self.complexes_viewer.AddItem((0,0), c, label=complex_name)
                self.update = True
            except Exception as e:
                message_window.error('can not add the two complexes because of the error:'+str(e))
                return
            
    def subtraction(self):
        if self.curr_complex is None:
            self.select_complex(comments='for subtraction(1)')
        other = self.select_complex(fresh_curr_complex=False, comments='for subtraction(2)')
        quit = False
        if self.curr_complex is None:
            message_window.error('the first complex of the subtraction did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second complex of subtraction did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                    'input complex name for the result', 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if complex_name is not None:
                if '>' in complex_name:
                    message_window.warning("you complex name includes '>', which is not allowed. system will create one randomly")
                    complex_name = random_string(5)
                if complex_name in self.all_complex_dict.keys():
                    message_window.warning('the name of the complex is included,system will add some random chars')
                    new_name = (complex_name + random_string(5))
                    while new_name in self.all_complex_dict.keys():
                        new_name = (complex_name + random_string(5))
                    complex_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one randomly')
                complex_name = random_string(7)
                while complex_name in self.all_complex_dict.keys():
                    complex_name = random_string(7)
            try:
                answer = ComplexSubtraction(complex(self.curr_complex[1]), complex(other[1]))
                answer = str(answer)
                self.all_complex_data.append((complex_name, answer))
                self.all_complex_dict[complex_name] = answer
                c = turn_complex_str_to_tuple(answer)
                self.complexes_viewer.AddItem((0,0), c, label=complex_name)
                self.update = True
            except Exception as e:
                message_window.error('can not add the two complexes because of the error:'+str(e))
                return

    def multiplication(self):
        if self.curr_complex is None:
            self.select_complex(comments='for multiplication(1)')
        other = self.select_complex(fresh_curr_complex=False, comments='for multiplication(2)')
        quit = False
        if self.curr_complex is None:
            message_window.error('the first complex of the multiplication did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second complex of multiplication did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                    'input complex name for the result', 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if complex_name is not None:
                if '>' in complex_name:
                    message_window.warning("you complex name includes '>', which is not allowed. system will create one randomly")
                    complex_name = random_string(5)
                if complex_name in self.all_complex_dict.keys():
                    message_window.warning('the name of the complex is included,system will add some random chars')
                    new_name = (complex_name + random_string(5))
                    while new_name in self.all_complex_dict.keys():
                        new_name = (complex_name + random_string(5))
                    complex_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one randomly')
                complex_name = random_string(7)
                while complex_name in self.all_complex_dict.keys():
                    complex_name = random_string(7)
            try:
                answer = ComplexMultiplication(complex(self.curr_complex[1]), complex(other[1]))
                answer = str(answer)
                self.all_complex_data.append((complex_name, answer))
                self.all_complex_dict[complex_name] = answer
                print(answer)
                c = turn_complex_str_to_tuple(answer)
                self.complexes_viewer.AddItem((0,0), c, label=complex_name)
                self.update = True
            except Exception as e:
                #raise e
                message_window.error('can not add the two complexes because of the error:'+str(e))
                return

    def division(self):
        if self.curr_complex is None:
            self.select_complex(comments='for division(1)')
        other = self.select_complex(fresh_curr_complex=False, comments='for division(2)')
        quit = False
        if self.curr_complex is None:
            message_window.error('the first complex of the division did NOT select correctly')
            quit = True
        if other is None:
            message_window.error('the second complex of division did NOT select correctly')
            quit = True
        if quit:
            return
        else:
            complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                    'input complex name for the result', 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if complex_name is not None:
                if '>' in complex_name:
                    message_window.warning("you complex name includes '>', which is not allowed. system will create one randomly")
                    complex_name = random_string(5)
                if complex_name in self.all_complex_dict.keys():
                    message_window.warning('the name of the complex is included,system will add some random chars')
                    new_name = (complex_name + random_string(5))
                    while new_name in self.all_complex_dict.keys():
                        new_name = (complex_name + random_string(5))
                    complex_name = new_name
            else:
                message_window.warning('you did not select a name! system will create one randomly')
                complex_name = random_string(7)
                while complex_name in self.all_complex_dict.keys():
                    complex_name = random_string(7)
            try:
                answer = ComplexDivision(complex(self.curr_complex[1]), complex(other[1]))
                answer = str(answer)
                self.all_complex_data.append((complex_name, answer))
                self.all_complex_dict[complex_name] = answer
                c = turn_complex_str_to_tuple(answer)
                self.complexes_viewer.AddItem((0,0), c, label=complex_name)
                self.update = True
            except Exception as e:
                message_window.error('can not add the two complexes because of the error:'+str(e))
                return

    def conjugate(self):
        if self.curr_complex is None:
            message_window.error('no current complex is selected')
            self.select_complex()
            return
        complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                   'input complex name for the result', 'OK',
                                                   'CANCEL', backgroundColor=(90, 90, 150),
                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        if complex_name is not None:
            if '>' in complex_name:
                message_window.warning(
                    "you complex name includes '>', which is not allowed. system will create one randomly")
                complex_name = random_string(5)
            if complex_name in self.all_complex_dict.keys():
                message_window.warning('the name of the complex is included,system will add some random chars')
                new_name = (complex_name + random_string(5))
                while new_name in self.all_complex_dict.keys():
                    new_name = (complex_name + random_string(5))
                complex_name = new_name
        else:
            message_window.warning('you did not select a name! system will create one randomly')
            complex_name = random_string(5)
            while complex_name in self.all_complex_dict.keys():
                complex_name = random_string(5)
        answer = ComplexConjugate(complex(self.curr_complex[1]))
        self.all_complex_dict[complex_name] = str(answer)
        self.all_complex_data.append([complex_name, str(answer)])
        c = turn_complex_str_to_tuple(str(answer))
        self.complexes_viewer.AddItem((0,0), c, label=complex_name)
        self.update = True

    def to_polar(self):
        if self.curr_complex is None:
            message_window.error('no current complex is selected')
            self.select_complex()
            return
        copy_answer = pyghelpers.textYesNoDialog(self.window, (0, 0, 1004, 300),
                                   'The Polar form(RAD) is:'+str(ComplexToPolar(self.curr_complex)),
                                   'copy', "cancel")
        if copy_answer:
            pyperclip.copy(str(ComplexToPolar(self.curr_complex)))

    def abs(self):
        if self.curr_complex is None:
            message_window.error('no current complex is selected')
            self.select_complex()
            return
        complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                   'input complex name for the result', 'OK',
                                                   'CANCEL', backgroundColor=(90, 90, 150),
                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        if complex_name is not None:
            if '>' in complex_name:
                message_window.warning(
                    "you complex name includes '>', which is not allowed. system will create one randomly")
                complex_name = random_string(5)
            if complex_name in self.all_complex_dict.keys():
                message_window.warning('the name of the complex is included,system will add some random chars')
                new_name = (complex_name + random_string(5))
                while new_name in self.all_complex_dict.keys():
                    new_name = (complex_name + random_string(5))
                complex_name = new_name
        else:
            message_window.warning('you did not select a name! system will create one randomly')
            complex_name = random_string(7)
            while complex_name in self.all_complex_dict.keys():
                complex_name = random_string(7)
        copy_answer = pyghelpers.textYesNoDialog(self.window, (0, 0, 1004, 300),
                                                 'The answer is:' + str(ComplexAbs(self.curr_complex[1])),
                                                 'copy', "cancel")
        if copy_answer:
            pyperclip.copy(str(ComplexAbs(self.curr_complex[1])))

    def angle(self):
        if self.curr_complex is None:
            message_window.error('no current complex is selected')
            self.select_complex()
            return

        copy_answer = pyghelpers.textYesNoDialog(self.window, (0, 0, 1004, 300),
                                                 'The angle(to the real axis) is:' + str(ComplexAngle(self.curr_complex[1])),
                                                 'copy', "cancel")
        if copy_answer:
            pyperclip.copy(str(ComplexAngle(self.curr_complex[1])))

    def change_curr_complex(self):
        if self.curr_complex is None:
            message_window.error('no complex is selected!');return
        changing_type_selector = CheckBox(2,
                                         ['reset value','RENAME'],
                                         1,
                                         self.window, self.clock, first_x=60, first_y=100, each_add_x=0, each_add_y=30,
                                         buttons_adjust_length=0, background_color=(90, 90, 150))
        if len(changing_type_selector.clicked_choices) == 0 or type(changing_type_selector.clicked_choices) == str:return
        choice = changing_type_selector.clicked_choices[0]

        if choice == 0:
            #reset value
            real = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200), 'input the real part of the complex', 'OK',
                                                          'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if real is None:
                message_window.error('no inputs is given.')
                return
            try:
                float(real)
            except:
                message_window.error('bad input for float:'+str(real))
                return
            imagine = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                               'input the imaginary value(do NOT contain "j)" of the complex', 'OK',
                                               'CANCEL', backgroundColor=(90, 90, 150),
                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if imagine is None:
                message_window.error('no inputs is given.')
                return
            try:
                float(imagine)
            except:
                message_window.error('bad input for float:' + str(imagine))
                return
            self.all_complex_data[self.all_complex_data.index(self.curr_complex)] [1] = str(complex(real + '+' + imagine + 'j'))
            self.curr_complex[1] = str(complex(real + '+' + imagine + 'j'))
            self.all_complex_dict[self.curr_complex[0]] = str(complex(real + '+' + imagine + 'j'))
        elif choice == 1:
            #rename
            name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                  'input the name of the complex', 'OK',
                                                  'CANCEL', backgroundColor=(90, 90, 150),
                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            if name is None:
                message_window.error('no inputs is given')
                return
            if name in self.all_complex_dict.keys():
                message_window.warning('the name is the same as others.system will add some random chars.')
                name += random_string(2)
                while name in self.all_complex_dict.keys():
                    name = name[0:len(name)-2]
                    name += random_string(2)
            del self.all_complex_dict[self.curr_complex[0]]
            self.all_complex_dict[name] = self.curr_complex[1]
            self.all_complex_data[self.all_complex_data.index(self.curr_complex)][0] = name
            self.curr_complex[0] = name
        self.update = True

    def copy_complex(self):
        if self.curr_complex is None:
            message_window.error('no complex is selected')
            return
        complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                  'input complex name for the result', 'OK',
                                                  'CANCEL', backgroundColor=(90, 90, 150),
                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        if complex_name is not None:
            if '|' in complex_name or '>' in complex_name or ';' in complex_name:
                message_window.warning(
                    "you complex name includes '|', '>' or ';', which is(are) not allowed. system will create one randomly")
                complex_name = random_string(5)
            if complex_name in self.all_complex_dict.keys():
                message_window.warning('the name of the complex is included,system will add some random chars')
                new_name = (complex_name + random_string(5))
                while new_name in self.all_complex_dict.keys():
                    new_name = (complex_name + random_string(5))
                complex_name = new_name
            self.all_complex_dict[complex_name] = self.curr_complex[1]
            self.all_complex_data.append([complex_name, self.curr_complex[1]])
            c = turn_complex_str_to_tuple(self.curr_complex[1])
            self.complexes_viewer.AddItem((0,0), c, label=complex_name)

        self.curr_complex_preview = WindowListViewer(self.curr_complex[1], (700, 420), self.window, (304, 190))
        self.curr_complex_title = self.curr_complex[0]
        self.curr_complex_preview_title = pygwidgets.TextButton(self.window, (304, 150), self.curr_complex_title,
                                                                fontName='fonts/JetBrainsMono-Light.ttf',
                                                                width=700,
                                                                upColor=(135, 206, 250),
                                                                downColor=(135, 206, 250),
                                                                overColor=(135, 206, 250))
        self.update = True

    def others(self):
        type_selector = CheckBox(5,
                                 ['Remove Current Complex', 'Complex Angle', 'Complex to Polar', 'Square Root', 'Cube Root'],
                                 1,
                                 self.window, self.clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30,
                                 buttons_adjust_length=0, background_color=(90, 90, 150))
        if type_selector.clicked_choices == 'cancel' or len(type_selector.clicked_choices) == 0:
            message_window.error('no choice is selected');return
        choice = type_selector.clicked_choices[0]
        self.update = True
        if choice == 0:
            if self.curr_complex is None:
                message_window.error('no current complex is selected!')
                self.select_complex()
                return
            Index = self.all_complex_data.index(self.curr_complex)
            del self.all_complex_data[Index]
            self.complexes_viewer.RemoveItem(Index, item_type=ARROW)
            del self.all_complex_dict[self.curr_complex[0]]
            self.curr_complex = None
            self.curr_matrix_title = 'No complex is selected'
            self.curr_matrix_preview_title = pygwidgets.TextButton(self.window, (304, 150), self.curr_matrix_title,
                                                                   fontName='fonts/JetBrainsMono-Light.ttf', width=700,
                                                                   upColor=(135, 206, 250), downColor=(135, 206, 250),
                                                                   overColor=(135, 206, 250))
        elif choice == 1:
            self.angle()
        elif choice == 2:
            self.to_polar()
        elif choice == 3 or choice == 4:
            if self.curr_complex is None:
                message_window.error('no current complex is selected')
                self.select_complex()
                return
            names = []
            for _ in range(2):
                complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                           'input complex name for the result('+str(_+1)+')'+(' for square root' if choice == 3 else ' for cube roots'), 'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                if complex_name is not None:
                    if '>' in complex_name:
                        message_window.warning(
                            "you complex name includes '>', which is not allowed. system will create one randomly")
                        complex_name = random_string(5)
                    if complex_name in self.all_complex_dict.keys():
                        message_window.warning('the name of the complex is included,system will add some random chars')
                        new_name = (complex_name + random_string(5))
                        while new_name in self.all_complex_dict.keys():
                            new_name = (complex_name + random_string(5))
                        complex_name = new_name
                else:
                    message_window.warning('you did not select a name! system will create one randomly')
                    complex_name = random_string(5)
                    while complex_name in self.all_complex_dict.keys():
                        complex_name = random_string(5)
                    names.append(complex_name)
            if choice == 3:
                # square root
                com = complex(self.curr_complex[1])
                answers = all_complex_square_roots(com)
                answers = [turn_complex_str_to_tuple(str(curr_answer)) for curr_answer in answers]
                for complex_name,answer in answers:
                    self.all_complex_dict[complex_name] = answer
                    self.all_complex_data.append([complex_name, answer])
            else:
                complex_name = pyghelpers.textAnswerDialog(self.window, (0, 0, 1004, 200),
                                                           'input complex name for the result(3) for cube roots',
                                                           'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                if complex_name is not None:
                    if '>' in complex_name:
                        message_window.warning(
                            "you complex name includes '>', which is not allowed. system will create one randomly")
                        complex_name = random_string(5)
                    if complex_name in self.all_complex_dict.keys():
                        message_window.warning('the name of the complex is included,system will add some random chars')
                        new_name = (complex_name + random_string(5))
                        while new_name in self.all_complex_dict.keys():
                            new_name = (complex_name + random_string(5))
                        complex_name = new_name
                else:
                    message_window.warning('you did not select a name! system will create one randomly')
                    complex_name = random_string(5)
                    while complex_name in self.all_complex_dict.keys():
                        complex_name = random_string(5)
                    names.append(complex_name)

                com = complex(self.curr_complex[1])
                answers = all_complex_cube_roots(com)
                answers = [turn_complex_str_to_tuple(str(answer)) for answer in answers]
                for complex_name, answer in answers:
                    self.all_complex_dict[complex_name] = answer
                    self.all_complex_data.append([complex_name, answer])

def turn_complex_str_to_tuple(string:str):
    """
    :param string: in forms like '(1+2j)'
    :return: tuple, like(1.0, 2.0)
    """
    if '(' in string and ')' in string:
        result = string[1:-2]
    else:
        result = string

    if '-' in result:
        result = result.split('-')
        result[1] = '-'+result[1]
        result = tuple([float(i) for i in result])
    elif '+' in result:
        result = result.split('+')
        result[1] = '+' + result[1]
        result = tuple([float(i) for i in result])
    else:
        # things like '4j'
        result = (0., float(result[0:-1]))
    return result


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
        b = ComplexUi(window, clock, (0, 0), 1004, 610, all_data=k)
        k = b.draw()
    pygame.quit()
    sys.exit(0)

