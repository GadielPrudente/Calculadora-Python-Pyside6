from PySide6.QtWidgets import (QApplication, QLabel)
from PySide6.QtGui import QIcon
from info import info
from display import Display
from buttons import buttun, buttunsGrid
from styles import setupTheme
from main_window import Mw
from variaveis import ICON
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Mw()
    setupTheme(app)
    # label1 = QLabel('calculadora')
    # label1.setStyleSheet('font-size: 50px')
    # window.addWidgetToVLayout(label1)
    icon = QIcon(str(ICON))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)
    innfo = info('2.0 / 6.0 = ')
    window.addWidgetToVLayout(innfo)



    display_var = Display() 
    window.addWidgetToVLayout(display_var)

    buttonsGrid = buttunsGrid(display_var, innfo, window)  
    window.vlayout.addLayout(buttonsGrid)



    window.adjustFixedSize() 
    window.show()
    app.exec()