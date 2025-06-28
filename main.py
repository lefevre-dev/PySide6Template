import sys
from PySide6.QtCore import QFile
# from PyQt5.QtGui import QPixmap
from pid.decorator import pidfile
from PySide6.QtWidgets import QApplication
from Front.Window.MainWindow import MainWindow
from Log.LogModule import DefaultLogger
import traceback
import Front.Ressources.ressources_rc


def except_hook(cls, exception, tb):
    DefaultLogger.get_instance().error("Uncaught exception " + str(exception))
    DefaultLogger.get_instance().error(traceback.format_exc())
    sys.__excepthook__(cls, exception, tb)


class LoggerWriter:
    def write(self, message):
        if message != '\n':
            DefaultLogger.get_instance().info(message)

    def flush(self):
        pass

@pidfile()
def main(args):

    # création du fichier de config s’il n’existe pas
    DefaultLogger.get_instance().info("Start soft")

    app = QApplication(args)

    # chargement du style
    file = QFile(":/Style/style.qss")
    if file.open(QFile.ReadOnly | QFile.Text):
        style_sheet = file.readAll().data().decode()
        app.setStyleSheet(style_sheet)

    # splashpix = QPixmap(':/Images/Images/seva_logo_splash.jpg')
    # splash = QSplashScreen(splashpix)
    # splash.show()
    app.processEvents()

    win = MainWindow()

    # splash.finish(win)
    win.showMaximized()
    app.exec()
    DefaultLogger.get_instance().info("Stop soft")



def start_main():
    # redirection des exceptions
    sys.excepthook = except_hook
    # redirection des prints
    sys.stdout = LoggerWriter()
    main(sys.argv)


if __name__ == '__main__':
    start_main()