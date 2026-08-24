#Projeto desenvolvido com colaboração.


from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit
from variaveis import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUN_WITH
from PySide6.QtCore import Qt, Signal
from utils import isEmpty, isNumOrDot

class Display(QLineEdit):
    eqRequested = Signal()
    delPressed = Signal()
    escPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configstyle()

    def configstyle(self):
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for _ in range(4)])
        self.setMinimumWidth(MINIMUN_WITH)


    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        isDel = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape]
        isOper = key in [KEYS.Key_Plus, KEYS.Key_Minus,
                        KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P]

        if isEnter:
            self.eqRequested.emit()
            return event.ignore() 

        if isDel:
            self.delPressed.emit()
            return event.ignore()

        if isOper:
            if text.lower() == 'p':
                text = '^'

            self.operatorPressed.emit(text)
            return event.ignore()

        if isEsc:
            self.escPressed.emit()
            return event.ignore()

        if isEmpty(text):
            return event.ignore()

        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()

        