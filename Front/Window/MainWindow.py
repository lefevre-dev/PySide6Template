from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow
from Front.UI.Window.ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    VERSION_ = "1.0.0"

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(f"SOFT (v{self.VERSION_})")
        self.setWindowIcon(QIcon(':Images/Images/qt_icon.ico'))
        self.translator = QtCore.QTranslator()