import sys

from configs import Display, Info, Button, ButtonsGrid
from PySide6.QtWidgets import QApplication
from mainwindows import MainWindow
from PySide6.QtGui import QIcon
from variables import WINDOW_ICON_PATH

#from style import setupTheme


if __name__ == '__main__':
    # snake_case
    # PascalCase
    # camelCase

    app = QApplication(sys.argv)
    window = MainWindow()

    # Define o icone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Labels
    info = Info('') 
    window.addWidgetToVLayout(info)

    
    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    # Butoões
   

    #setupTheme()


    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()