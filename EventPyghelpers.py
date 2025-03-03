"""
************************************************************************************************

Simplified BSD License:

Copyright 2017 Irv Kalb. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY Irv Kalb ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Irv Kalb OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Irv Kalb.

-----------------------------------------------------------------------------------------

And the following functions ARE MODIFIED OR ADDED by TSKR Mike under the License of Irv Kalb.
Copyright 2025 TSKR-Mike. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY TSKR Mike ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Irv Kalb OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of TSKR Mike.
TSKR-Mike@www.github.com
******************************************************************************************
"""

DIALOG_BACKGROUND_COLOR = (0, 200, 200)
DIALOG_BLACK = (0, 0, 0)
import pygame
from pygame.locals import *
import pygwidgets
import sys
import time
import os
from abc import ABC, abstractmethod


def textYesNoDialogEventProgressing(theWindow, theRect, prompt, drawFuncs: list, eventHandlerFuncs: list,
                                    yesButtonText='Yes', noButtonText='No', backgroundColor=DIALOG_BACKGROUND_COLOR,
                                    textColor=DIALOG_BLACK):
    """A function that puts up a text-based two-button modal dialog (typically Yes/No or OK/Cancel)

    It can also be used to put up a single button alert dialog (typically with an OK button)

    Parameters:
        |    theWindow - the window to draw in
        |    theRect - the rectangle (or tuple) of the dialog box in the application window
        |    prompt - prompt (title) string to be displayed in the dialog box

    Optional keyword parameters:
        |    yesButtonText - text on the Yes button (defaults to 'Yes')
        |    noButtonText - text on the No button (defaults to 'No')
        |       Note:  If noButtonText is None, the nothing will be drawn for the No button
        |              This way, you can present an "alert" box with only an 'OK' button
        |    backgroundColor - rgb background color for the dialog box (defaults to (0, 200, 200))
        |    textColor - rgb color for the prompt text (defaults to black)

    Returns:
        |    True - meaning the Yes button was pressed
        |        or
        |    False - meaning the No button was pressed
        |
        |   (With an alert dialog, you can ignore the returned value, as it will always be True.)

    """
    dialogLeft = theRect[0]
    dialogTop = theRect[1]
    dialogWidth = theRect[2]
    dialogHeight = theRect[3]
    frameRect = pygame.Rect(dialogLeft + 1, dialogTop + 1, dialogWidth - 2, dialogHeight - 2)
    INSET = 30  # inset buttons from the edges of the dialog box

    promptText = pygwidgets.DisplayText(theWindow, (dialogLeft, dialogTop + 30), prompt,
                                        fontSize=24, width=dialogWidth, justified='center', textColor=textColor)

    # Create buttons, fix locations after finding out the size of the button(s)
    showNoButton = not (noButtonText is None)
    if showNoButton:
        noButton = pygwidgets.TextButton(theWindow, (0, 0), noButtonText)
    yesButton = pygwidgets.TextButton(theWindow, (0, 0), yesButtonText)

    yesButtonRect = yesButton.getRect()
    yesButtonHeight = yesButtonRect[3]
    yesButtonWidth = yesButtonRect[2]  # get width
    xPos = dialogLeft + dialogWidth - yesButtonWidth - INSET
    buttonsY = dialogTop + dialogHeight - yesButtonHeight - 20
    if showNoButton:
        noButton.setLoc((dialogLeft + INSET, buttonsY))
    yesButton.setLoc((xPos, buttonsY))

    #print('In dialogYesNo')
    #print('theRect is', theRect)
    #print('frameRect is', frameRect)

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                    ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if showNoButton:
                if noButton.handleEvent(event):
                    return False

            if yesButton.handleEvent(event):
                return True

            for func in eventHandlerFuncs:
                func(event)

        for func in drawFuncs:
            func()

        # 8 - Do any "per frame" actions

        # 9 - Clear the window area before drawing it again
        pygame.draw.rect(theWindow, backgroundColor, theRect)
        pygame.draw.rect(theWindow, DIALOG_BLACK, frameRect, 1)

        # 10 - Draw the window elements
        promptText.draw()
        if showNoButton:
            noButton.draw()
        yesButton.draw()

        # 11 - Update the window
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def customYesNoDialogEventProgressing(theWindow, oDialogImage, oPromptText, oYesButton, drawFuncs, eventHandlerFuncs,
                                      oNoButton=None):
    """A function that puts up a custom two-button modal dialog (typically Yes/No or OK/Cancel)

    It can also be used to put up a single button alert dialog (with a typcial OK button)

    Parameters:
        |    theWindow - the window to draw in
        |    oDialogImage - an Image object (from pygwidgets) with the background of the dialog box
        |    oPromptText - a TextDisplay object (from pygwidgets) containing the prompt to display
        |    oYesButton - a CustomButton object (from pygwidgets) representing Yes or OK, etc.

    Optional keyword parameter:
        |    oNoButton - a CustomButton object (from pygwidgets) representing No or Cancel, etc. (default None)
        |       Note:  If oNoButton is None, the No button will not be drawn
        |              This way, you can present an "alert" box with only a single button, like 'OK'

    Returns:
        |    True - meaning the Yes button was pressed
        |        or
        |    False - meaning the No button was pressed
        |
        |   (With an alert dialog, you can ignore the returned value, as it will always be True.)

    """

    showNoButton = not (oNoButton is None)

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                    ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if showNoButton:
                if oNoButton.handleEvent(event):
                    return False

            if oYesButton.handleEvent(event):
                return True
            for func in eventHandlerFuncs:
                func(event)

        for func in drawFuncs:
            func()

        # 8 - Do any "per frame" actions

        # 9 - Clear the window area before drawing it again

        # 10 - Draw the window elements
        oDialogImage.draw()
        oPromptText.draw()
        if showNoButton:
            oNoButton.draw()
        oYesButton.draw()

        # 11 - Update the window
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def textAnswerDialogEventProgressing(theWindow, theRect, prompt, drawFuncs, eventHandlerFuncs, okButtonText='OK',
                                     cancelButtonText='Cancel', backgroundColor=DIALOG_BACKGROUND_COLOR,
                                     promptTextColor=DIALOG_BLACK, inputTextColor=DIALOG_BLACK):
    """A function that puts up a text-based two-button answerable modal dialog (typically OK/Cancel)

    Parameters:
        |    theWindow - the window to draw in
        |    theRect - the rectangle (or tuple) of the dialog box in the application window
        |    prompt - prompt (title) string to be displayed in the dialog box

    Optional keyword parameters:
        |    okButtonText - text on the OK button (defaults to 'OK')
        |    cancelButtonText - text on the Cancel button (defaults to 'Cancel')
        |    backgroundColor - rgb background color for the dialog box (defaults to (0, 200, 200))
        |    promptTextColor - rgb color of the prompt text (defaults to black)
        |    inputTextColor - rgb color of the input text (defaults to black)

    Returns:
         |   userAnswer - If user presses OK, returns the text the user typed. Otherwise, returns None

    """

    dialogLeft = theRect[0]
    dialogTop = theRect[1]
    dialogWidth = theRect[2]
    dialogHeight = theRect[3]
    INSET = 30  # inset buttons from the edges of the dialog box

    promptText = pygwidgets.DisplayText(theWindow, (dialogLeft, dialogTop + 30), prompt,
                                        fontSize=24, width=dialogWidth, justified='center',
                                        textColor=promptTextColor)

    inputWidth = dialogWidth - (2 * INSET)
    inputText = pygwidgets.InputText(theWindow, (dialogLeft + INSET, dialogTop + 80),
                                     width=inputWidth, initialFocus=True, textColor=inputTextColor)

    cancelButton = pygwidgets.TextButton(theWindow, (0, 0), cancelButtonText)
    okButton = pygwidgets.TextButton(theWindow, (0, 0), okButtonText)

    okButtonRect = okButton.getRect()
    okButtonHeight = okButtonRect[3]
    okButtonWidth = okButtonRect[2]  # get width
    xPos = dialogLeft + dialogWidth - okButtonWidth - INSET
    buttonsY = dialogTop + dialogHeight - okButtonHeight - 20
    cancelButton.setLoc((dialogLeft + INSET, buttonsY))
    okButton.setLoc((xPos, buttonsY))

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                    ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if inputText.handleEvent(event) or okButton.handleEvent(event):
                theAnswer = inputText.getValue()
                return theAnswer

            if cancelButton.handleEvent(event):
                return None

            for func in eventHandlerFuncs:
                func(event)

        for func in drawFuncs:
            func()

        # 8 - Do any "per frame" actions

        # 9 - Clear the window area before drawing it again
        pygame.draw.rect(theWindow, backgroundColor, theRect)
        pygame.draw.rect(theWindow, DIALOG_BLACK, theRect, 1)

        # 10 - Draw the window elements
        promptText.draw()
        inputText.draw()
        cancelButton.draw()
        okButton.draw()

        # 11 - Update the window
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


def customAnswerDialogEventProgressing(theWindow, oDialogImage, oPromptText, oAnswerText, oOKButton, oCancelButton,
                                       drawFuncs, eventHandlerFuncs):
    """A function that puts up a custom two-button modal dialog (typically Yes/No or OK/Cancel)

    Parameters:
        |    theWindow - the window to draw in
        |    oDialogImage - an Image object (from pygwidgets) containing the background of the dialog box
        |    oPromptText - a TextDisplay object (from pygwidgets) containing the prompt to display
        |    oAnswerText - an InputText object (from pygwidgets) where the user types their answer
        |    oOKButton - a CustomButton object (from pygwidgets) representing OK, etc.
        |    oCancelButton - a CustomButton object (from pygwidgets) representing Cancel, etc.

    Returns:
         |    userAnswer - If user presse OK, returns the text the user typed. Otherwise, returns None

    """

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                    ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if oAnswerText.handleEvent(event) or oOKButton.handleEvent(event):
                userResponse = oAnswerText.getValue()
                return userResponse

            if oCancelButton.handleEvent(event):
                return None

            for func in eventHandlerFuncs:
                func(event)
        for func in drawFuncs:
            func()

        # 8 - Do any "per frame" actions

        # 9 - Clear the window area before drawing it again

        # 10 - Draw the window elements
        oDialogImage.draw()
        oAnswerText.draw()
        oPromptText.draw()
        oCancelButton.draw()
        oOKButton.draw()

        # 11 - Update the window
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this


LEGAL_KEYS = (
    pygame.K_RIGHT, pygame.K_LEFT, pygame.K_HOME, pygame.K_END, pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_RETURN,
    pygame.K_KP_ENTER)
LEGAL_UNICODES = '1234567890-.'


class InputNumber(pygwidgets.InputText):
    def __init__(self, window, loc, value='', fontName=None, fontSize=24, width=200, text_color=(0, 0, 0),
                 bkg_color=(255, 255, 255), ALLOW_FLOAT=True, ALLOW_NEGATIVE=True):
        super().__init__(window, loc, value, fontName, fontSize, width, text_color, bkg_color, initialFocus=True)
        self.allow_float, self.allow_negative = ALLOW_FLOAT, ALLOW_NEGATIVE

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if not ((event.key in LEGAL_KEYS) or (event.unicode in LEGAL_UNICODES)): return False
            if event.unicode == '-':
                if not self.allow_negative: return False
                if self.cursorPosition > 0: return False  #'-' can only be added in front of a char
                if '-' in self.text: return False
            elif event.unicode == '.':
                if not self.allow_float: return False
                if '.' in self.text: return False

        result = super().handleEvent(event)
        return result

    def getValue(self):
        userString = super().getValue()
        try:
            if self.allow_float:
                return_value = float(userString)
            else:
                return_value = int(userString)
        except ValueError:
            return None
        return return_value


def textNumberDialogEventProgressing(theWindow, theRect, prompt, drawFuncs=None, eventHandlerFuncs=None,
                                     okButtonText='OK', cancelButtonText='Cancel', backgroundColor=DIALOG_BACKGROUND_COLOR,
                                     promptTextColor=DIALOG_BLACK, inputTextColor=DIALOG_BLACK, allow_negative=True,
                                     allow_float=True):
    """A function that puts up a text-based two-button answerable modal dialog (typically OK/Cancel)

    Parameters:
        |    theWindow - the window to draw in
        |    theRect - the rectangle (or tuple) of the dialog box in the application window
        |    prompt - prompt (title) string to be displayed in the dialog box

    Optional keyword parameters:
        |    okButtonText - text on the OK button (defaults to 'OK')
        |    cancelButtonText - text on the Cancel button (defaults to 'Cancel')
        |    backgroundColor - rgb background color for the dialog box (defaults to (0, 200, 200))
        |    promptTextColor - rgb color of the prompt text (defaults to black)
        |    inputTextColor - rgb color of the input text (defaults to black)

    Returns:
         |   userAnswer - If user presses OK, returns the text the user typed. Otherwise, returns None

    """

    if eventHandlerFuncs is None:
        eventHandlerFuncs = []
    if drawFuncs is None:
        drawFuncs = []

    dialogLeft = theRect[0]
    dialogTop = theRect[1]
    dialogWidth = theRect[2]
    dialogHeight = theRect[3]
    INSET = 30  # inset buttons from the edges of the dialog box

    promptText = pygwidgets.DisplayText(theWindow, (dialogLeft, dialogTop + 30), prompt,
                                        fontSize=24, width=dialogWidth, justified='center',
                                        textColor=promptTextColor)

    inputWidth = dialogWidth - (2 * INSET)
    inputText = InputNumber(theWindow, (dialogLeft + INSET, dialogTop + 80),
                            width=inputWidth, text_color=inputTextColor, ALLOW_NEGATIVE=allow_negative,
                            ALLOW_FLOAT=allow_float)

    cancelButton = pygwidgets.TextButton(theWindow, (0, 0), cancelButtonText)
    okButton = pygwidgets.TextButton(theWindow, (0, 0), okButtonText)

    okButtonRect = okButton.getRect()
    okButtonHeight = okButtonRect[3]
    okButtonWidth = okButtonRect[2]  # get width
    xPos = dialogLeft + dialogWidth - okButtonWidth - INSET
    buttonsY = dialogTop + dialogHeight - okButtonHeight - 20
    cancelButton.setLoc((dialogLeft + INSET, buttonsY))
    okButton.setLoc((xPos, buttonsY))

    # 6 - Loop forever
    while True:

        # 7 - Check for and handle events
        for event in pygame.event.get():
            if (event.type == QUIT) or \
                    ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()

            if inputText.handleEvent(event) or okButton.handleEvent(event):
                theAnswer = inputText.getValue()
                return theAnswer

            if cancelButton.handleEvent(event):
                return None

            for func in eventHandlerFuncs:
                func(event)

        for func in drawFuncs:
            func()

        # 8 - Do any "per frame" actions

        # 9 - Clear the window area before drawing it again
        pygame.draw.rect(theWindow, backgroundColor, theRect)
        pygame.draw.rect(theWindow, DIALOG_BLACK, theRect, 1)

        # 10 - Draw the window elements
        promptText.draw()
        inputText.draw()
        cancelButton.draw()
        okButton.draw()

        # 11 - Update the window
        pygame.display.update()

        # 12 - Slow things down a bit
        #clock.tick(FRAMES_PER_SECOND)  # no need for this
