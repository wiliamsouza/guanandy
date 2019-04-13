#!/usr/bin/env python

import sys
import logging

from PySide2 import QtCore, QtWidgets

from Guanandy.Student.Views import StudentView

def start():

    app = QtWidgets.QApplication(sys.argv)

    #locale = QtCore.QLocale.system()
    #translator = QtCore.QTranslator()

    #i18n_file = '' + locale.name() + '.qm'
    #i18n_path = ''

    #if (translator.load(i18n_file, i18n_path)):
    #    app.installTranslator(translator)

    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)

    studentView = StudentView()
    studentView.show()
    app.exec_()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start()
