from PyQt5 import QtCore


class TranslatableWidget:


    def changeEvent(self, a0):
        if a0.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi(self)
