from PySide6.QtWidgets import (QMainWindow, QMessageBox,
                               QWidget, QVBoxLayout)

class Mw(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.cw = QWidget()
        self.vlayout = QVBoxLayout()
        self.cw.setLayout(self.vlayout)
    
        self.setCentralWidget(self.cw)
        self.setWindowTitle('CALCULADORA')



    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vlayout.addWidget(widget)


    def makeMsgBox(self):
        return QMessageBox(self)    