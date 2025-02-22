import pygwidgets


class ChoiceCenter:
    def __init__(self, window, Loc, texts, values, number, max_num=1, soundOnClick=None, firstlocX=None,
                 firstlocY=None, eachAddX=None, eachAddY=None, text_color='(0, 0, 0)', font=None, fontSize=20):
        self.clicked_choices = []
        self.choices = []  # 储存所有选项
        self.window = window
        self.Loc = Loc
        self.texts = texts
        self.values = values
        self.number = number
        self.fontsize = fontSize
        self.font = font
        self.sound = soundOnClick
        self.max_choices = max_num
        self.text_color = [(0, 0, 0) for i in range(number)]
        self.i = 0
        self.Object = 0
        self.locX = firstlocX
        self.locY = firstlocY
        self.eachAddX = eachAddX
        self.eachAddY = eachAddY
        if self.locX is None:
            if self.sound is None:
                for i in range(number):
                    self.Object = pygwidgets.TextRadioButton(self.window, self.Loc[i], 1, self.texts[i],
                                                             self.values[i], fontSize=self.fontsize,
                                                             textColorDeselected=self.text_color[i],
                                                             textColorSelected=self.text_color[i], fontName=self.font)
                    self.choices.append(self.Object)
            else:
                for i in range(number):
                    self.Object = pygwidgets.TextRadioButton(self.window, self.Loc[i], 1, self.texts[i],
                                                             self.values[i], fontSize=self.fontsize,
                                                             soundOnClick=self.sound,
                                                             textColorDeselected=self.text_color[i],
                                                             textColorSelected=self.text_color[i], fontName=self.font)
                    self.choices.append(self.Object)
        else:
            if self.sound is None:
                for i in range(number):
                    self.Object = pygwidgets.TextRadioButton(self.window, (self.locX, self.locY), 1, self.texts[i],
                                                             self.values[i], fontSize=self.fontsize,
                                                             textColorDeselected=self.text_color[i],
                                                             textColorSelected=self.text_color[i], fontName=self.font)
                    self.choices.append(self.Object)
                    self.locX += self.eachAddX
                    self.locY += self.eachAddY
            else:
                for i in range(number):
                    self.Object = pygwidgets.TextRadioButton(self.window, (self.locX, self.locY), 1, self.texts[i],
                                                             self.values[i], fontSize=self.fontsize,
                                                             soundOnClick=self.sound, fontName=self.font,
                                                             textColorDeselected=self.text_color[i],
                                                             textColorSelected=self.text_color[i])
                    self.choices.append(self.Object)
                    self.locX += self.eachAddX
                    self.locY += self.eachAddY

    def draw(self):
        for Object in self.choices:
            Object.draw()

    def get_clicked_choices(self):
        return [m for k, m in zip(self.values, range(len(self.values))) if k is True]

    def check_values(self,event):
        click_choice = None
        for i, loc in zip(self.choices, range(len(self.choices))):
            if i.handleEvent(event):
                click_choice = loc
                if self.values[loc]:
                    self.values[loc] = False

                else:
                    self.values[loc] = True
        for i, loc in zip(self.choices, range(len(self.choices))):
            i.setValue(self.values[loc])
        for i, loc in zip(self.choices, range(len(self.choices))):
            if self.values[loc] is True and loc not in self.clicked_choices:
                self.clicked_choices.append(loc)
        for i, loc in zip(self.choices, range(len(self.choices))):
            if self.values[loc] is False and loc in self.clicked_choices:
                del self.clicked_choices[self.clicked_choices.index(self.choices.index(i))]
        while len(self.clicked_choices) > self.max_choices:
            if click_choice is not None:
                del self.clicked_choices[0]
        for i, loc in zip(self.choices, range(len(self.choices))):
            if loc not in self.clicked_choices:
                i.setValue(False)
            else:
                i.setValue(True)
        for i, loc in zip(self.values, range(len(self.values))):
            if i is True:
                if loc not in self.clicked_choices:
                    self.values[loc] = False
                else:
                    self.values[loc] = True
            else:
                if loc in self.clicked_choices:
                    self.values[loc] = True
                else:
                    self.values[loc] = False

if __name__ == "__main__":
    import pygame
    import sys
    import pygwidgets

    window = pygame.display.set_mode((1000, 600))
    clock = pygame.time.Clock()
    o = ChoiceCenter(window, None, ['1111', '2', '3'], [False, False, False], 3,1,
                     firstlocX=100, firstlocY=20,eachAddX=45,eachAddY=0)
    while True:
        for event in pygame.event.get():
            window.fill((0, 191, 255))
            o.check_values(event)
            o.draw()
            pygame.display.update()
            clock.tick(10)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


