from PySide6.QtWidgets import QLineEdit, QLabel, QWidget, QPushButton, QGridLayout
from variables import isValidNumber, BIG_FONT_SIZE, DEFAULT_TEXT_MARGIN, MINIMUN_WIDHT, SMALL_FONT_SIZE, MEDIUM_FONT_SIZE, isEmpty, isNumOrDot
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QKeyEvent

import math
from mainwindows import MainWindow

class Display(QLineEdit):
    eqTriggered = Signal()
    delTriggered = Signal()
    clearTriggered = Signal()
    inputTriggered = Signal(str)
    operatorTriggered = Signal(str)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
        

    def configStyle(self):
        margins = [DEFAULT_TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUN_WIDHT)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete, KEYS.Key_D]
        isEsq = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P,]

        if isEnter:
            self.eqTriggered.emit()
            return event.ignore()

        if isDelete:
            self.delTriggered.emit()
            return event.ignore()
        
        if isEsq:
            self.clearTriggered.emit()
            return event.ignore()

        if isOperator:
            if text.lower() == 'p':
                text = '^'
            self.operatorTriggered.emit(text)
            return event.ignore()

        # Não passar daqui se não tiver texto
        if isEmpty(text):
            return event.ignore()


        if isNumOrDot(text):
            self.inputTriggered.emit(text)
            return event.ignore()


class Info(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyleInfo()

    def configStyleInfo(self):
        self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)
        


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, window: MainWindow, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['.',  '0', '-N', '='],  
        ]

        self.display = display 
        self.info = info
        self.window = window
        self._equation = ''
        self._left = None
        self._right = None
        self._operator = None
        self._equationInitialValue = ''
        self._gridMaker()

    
    @property
    def equation(self):                                               # SAO OS CONSTRUTORES DA EQUAÇÃO.
        return self._equation


    @equation.setter                                                
    def equation(self, value):
        self._equation = value
        self.info.setText(value)


    def vouApagarVocê(self, *args):
        print(f'sinal{args}: ', type(self).__name__)


    def _gridMaker(self):   
        self.display.eqTriggered.connect(self._eq)
        self.display.delTriggered.connect(self._backspace)
        self.display.clearTriggered.connect(self._clear)
        self.display.inputTriggered.connect(self._insertTextToDisplay)
        self.display.operatorTriggered.connect(self._operatorSelected)
                                                                     
        for rowNumber, row in enumerate(self._grid_mask):           # CRIOU O GRID COM O NUMERO DE COLUNAS E LINHAS DA MASCARA
            for columnNumber, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButtom(button)


                self.addWidget(button, rowNumber, columnNumber)
                Slot = self._makeSlot(
                    self._insertTextToDisplay, buttonText,
                )
                self._connectButtomClicked(button, Slot)


    def _connectButtomClicked(self, button, slot):
        button.clicked.connect(slot)


    def _configSpecialButtom(self, button):                     # CONECTA OS BUTÕES ESPECIAIS (NÃO NUMEROS) AS FUNÇÕES
        text = button.text()

        if text == 'C':
            self._connectButtomClicked(button, self._clear)

        if text == '◀':
            self._connectButtomClicked(button, self.display.backspace)

        if text in '+-/*^':
            self._connectButtomClicked(button, self._makeSlot(self._operatorSelected, text))

        if text == '=':
            self._connectButtomClicked(button, self._eq)
        
        if text == '-N':
            self._connectButtomClicked(button, self._negativeNumber)


    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot
    

    @Slot()
    def _insertTextToDisplay(self, text):         # INSERE OS BOTÕES NO DISPLAY
        newDisplayValue = self.display.text() + text
        self.display.setFocus()

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()


    @Slot()
    def _clear(self):                               # LIMPA O DISPLAY
        self._left = None
        self._right = None
        self._operator = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()


    @Slot()
    def _operatorSelected(self, text):                                     # ESSA FUNÇÃO CHECA SE O O OPERADOR FOI CLICADO E O COLOCA NO DISPLAY
        displayText = self.display.text()   # deverá ser self._left
        self.display.clear()    
        self.display.setFocus()

        if not isValidNumber(displayText) and self._left is None:
            return
        
        if self._left is None:
            self._left = float(displayText)

        self._operator = text
        self.equation = f'{self._left} {self._operator}'
        


    @Slot()
    def _negativeNumber(self):
        displayText = self.display.text()
        
        if not isValidNumber(displayText):
            return
        
        newNumber = -float(displayText)
        self.display.setText(str(newNumber))


    @Slot()
    def _eq(self):                                          # ESSA FUNÇÃO COLOCA OS VALORES APERTADOS NO DISPLAY DA CALCULADORA
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError('Conta incompleta.')
            return
        
        self._right = float(displayText)
        self.equation = f'{self._left} {self._operator} {self._right}'

        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
                
        except ZeroDivisionError:
            self._showError('Divisão por zero.')

        except OverflowError:
            self._showError('Excedeu o limite de números.')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == 'error':
            self._left = None
        



    def _makeDialogue(self, msg):                                # ESSA FUNÇÃO CRIA UM "ESPAÇO" PARA AS FUNÇÕES ABAIXO" 
        msgBox = self.window.messageBox()
        msgBox.setText(msg)
        return msgBox


    def _showError(self, msg):                                  # ESSA FUNÇÃO MOSTRA UMA MENSAGEM DE ERRO
        msgBox = self._makeDialogue(msg)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()


    def _showInfo(self, msg):                                   # ESSA FUNÇÃO MOSTRA UMA MENSAGEM DE INFORMAÇÃO
        msgBox = self._makeDialogue(msg)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
