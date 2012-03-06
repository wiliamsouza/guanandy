#!/usr/bin/env python

import sys

from PySide import QtCore, QtGui

from Classroom.Views.Qt.Student import StudentView

def start():

    app = QtGui.QApplication(sys.argv)

    #locale = QtCore.QLocale.system()
    #translator = QtCore.QTranslator()

    #i18n_file = '' + locale.name() + '.qm'
    #i18n_path = ''

    #if (translator.load(i18n_file, i18n_path)):
    #    app.installTranslator(translator)

    QtGui.QApplication.setQuitOnLastWindowClosed(False)

    studentView = StudentView()
    studentView.show()
    app.exec_()


if __name__ == '__main__':
    start()
