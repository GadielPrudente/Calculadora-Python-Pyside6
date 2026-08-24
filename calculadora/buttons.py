
#Projeto desenvolvido com colaboração.


import math
from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variaveis import MEDIUM_FONT_SIZE
from typing import TYPE_CHECKING
from utils import isEmpty, isNumOrDot, isValidNumbe

if TYPE_CHECKING:
    from main_window import Mw
    from display import Display
    from info import info
    

class buttun(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configstyle()

    def configstyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        font.setItalic(True)
        self.setMinimumSize(75, 75)
        self.setFont(font)

class buttunsGrid(QGridLayout):
    def __init__(self, display: Display, info: info, window: Mw, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gridMask = [
                ['C', 'D', '^', '/'],
                ['7', '8', '9', '*'],
                ['4', '5', '6', '-'],
                ['1', '2', '3', '+'],
                ['N',  '0', '.', '='],
            ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialVallue = 'sua conta'
        self._left = None
        self._right = None
        self.op = None
        self.equation = self._equationInitialVallue
        self.makeGrid()



    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)


    def makeGrid(self):
        self.display.eqRequested.connect(self._eq)
        self.display.delPressed.connect(self.display.backspace)
        self.display.escPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertBottonText)
        self.display.operatorPressed.connect(self._operatorClicked)
    

        for rowNumber, rowData in enumerate(self.gridMask):
            for collumNumber, buttonText in enumerate(rowData):
                button = buttun(buttonText)

                if not isNumOrDot(buttonText):
                    button.setProperty("cssClass", "specialButton")
                    self._confgSpecialButton(button)

                self.addWidget(button, rowNumber, collumNumber)
                Slot = self.makeButtonDisplay(self._insertBottonText,
                                                    buttonText)
                self._connectButtonClicked(button, Slot)

    def _connectButtonClicked(self,button, slot):
        button.clicked.connect(slot)


    def _confgSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text == 'N':
            self._connectButtonClicked(button, self._invert)

        if text in '+-/*^':
            self._connectButtonClicked(button, 
                                       self.makeButtonDisplay(
                                           self._operatorClicked, button))

        if text in '=':
            self._connectButtonClicked(button, self._eq)

        if text in 'D':
            self._connectButtonClicked(button, self.display.backspace)


    @Slot()
    def makeButtonDisplay(self, method, *args, **kwargs):

        @Slot(bool)
        def realSlot(_):
            method( *args, **kwargs)
        return realSlot
            

    @Slot()
    def _insertBottonText(self, text):

        newDisplayVallue = self.display.text() + text

        if not isValidNumbe(newDisplayVallue):
            return 

        self.display.insert(text)

    @Slot()
    def _invert(self):
        displayText = self.display.text()

        if not isValidNumbe(displayText):
            return 
        
        newNunber = float(displayText) * -1

        if newNunber.is_integer():
            newNunber = int(newNunber)

        self.display.setText(str(newNunber))

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self.op = None
        self.equation = self._equationInitialVallue
        self.display.clear()


    @Slot()
    def _operatorClicked(self, text):
        displyText = self.display.text()
        self.display.clear()

        if not isValidNumbe(displyText) and self._left is None:
            self.showError('não possui valor')
            return

        if self._left is None:
            self._left = float(displyText)

        self.op = text
        self.equation = f'{self._left} {self.op} !!'

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumbe(displayText) or self._left == None:
            self.showError('voçe não digitou nada')
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self.op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
                

            else:
                result = eval(self.equation)

        except ZeroDivisionError:
            self.showError('não se deve dividir por zero')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None  

        if result == 'error':
            self._left = None  
        

    def showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

