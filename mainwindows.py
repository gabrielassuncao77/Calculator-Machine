import sys
from typing import Optional
from PySide6.QtWidgets import  QMainWindow, QVBoxLayout, QWidget, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout) 
        self.setCentralWidget(self.cw)

        #Titulo da janela
        self.setWindowTitle('Calculadora')

        # Ultima coisa a ser feita
    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)

    def messageBox(self):
        return QMessageBox(self)