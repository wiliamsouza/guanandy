#!/usr/bin/env python

import sys

from PySide import QtCore, QtGui

from Classroom.Views.Qt.Teacher import ClassroomView

def start():

    app = QtGui.QApplication(sys.argv)

    #locale = QtCore.QLocale.system()
    #translator = QtCore.QTranslator()

    #i18n_file = '' + locale.name() + '.qm'
    #i18n_path = ''

    #if (translator.load(i18n_file, i18n_path)):
    #    app.installTranslator(translator)

    classroomView = classroomView()
    classroomView.show()
    classroomView.login()
    app.exec_()


if __name__ == '__main__':
    start()
