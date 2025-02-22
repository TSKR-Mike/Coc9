import pygwidgets


class ButtonCenter:
    """
        ButtonsLoc(List),textcolor=(0,0,0),upcolor,overcolor,downcolor,number,text(List),window,width, height,firstLocX=None,firstLocY=None,eachAddX=None,eachAddY=None,callbacks(List)
        该类能够批量创建并管理大量的按钮
    """
    
    def __init__(self, ButtonsLoc, textcolor, upcolor, overcolor, downcolor, number, text, window, width, height,
                 firstLocX=None, firstLocY=None, eachAddX=None, eachAddY=None, callbacks=None, font=None, font_size=20):
        self.Buttons = []  # 初始化储存所有按钮的信息的列表
        self.textcolor = textcolor
        self.up_color = upcolor
        self.over_color = overcolor
        self.down_color = downcolor
        self.font = font
        self.number = number
        self.window = window
        self.firstLocX = firstLocX
        self.firstLocY = firstLocY
        self.text = text
        self.eachAddX = eachAddX
        self.eachAddY = eachAddY
        self.font_size = font_size
        self.buttonX = firstLocX
        self.buttonY = firstLocY
        self.callbacks = callbacks
        self.ButtonsLoc = ButtonsLoc
        self.b = 0
        self.width = width
        self.height = height
        for self.b in range(self.number):  # 实例化所有按钮
            if callbacks is not None:
                if self.firstLocX is not None:
                    self.objectButton = pygwidgets.TextButton(window, (self.buttonX, self.buttonY), self.text[self.b],
                                                              self.width, self.height, self.textcolor, self.up_color,
                                                              self.over_color, self.down_color, fontName=self.font, fontSize=self.font_size,
                                                              callBack=self.callbacks[self.b])
                    self.buttonX += self.eachAddX
                    self.buttonY += self.eachAddY
                elif self.ButtonsLoc is not None:
                    self.objectButton = pygwidgets.TextButton(window, self.ButtonsLoc[self.b], self.text[self.b],
                                                              self.width, self.height, self.textcolor, self.up_color,
                                                              self.over_color, self.down_color, fontName=self.font, fontSize=self.font_size,
                                                              callBack=self.callbacks[self.b])
            else:
                if self.firstLocX is not None:
                    self.objectButton = pygwidgets.TextButton(window, (self.buttonX, self.buttonY), self.text[self.b],
                                                              self.width, self.height, self.textcolor
                                                              , self.up_color, self.over_color, self.down_color, fontName=self.font, fontSize=self.font_size)
                    self.buttonX += eachAddX
                    self.buttonY += eachAddY
                elif self.ButtonsLoc is not None:
                    self.objectButton = pygwidgets.TextButton(window, self.ButtonsLoc[self.b], self.text[self.b],
                                                              self.width, self.height, self.textcolor
                                                              , self.up_color, self.over_color, self.down_color, fontName=self.font, fontSize=self.font_size)
            self.Buttons.append(self.objectButton)  # 添加按钮的信息
    
    def drawAllButtons(self):
        for Object in self.Buttons:
            Object.draw()
