#!/usr/bin/env python

import sys
import logging

from PySide import QtCore, QtGui

from Guanandy.Teacher.Views import TeacherView


def start():

    app = QtGui.QApplication(sys.argv)

    icon = QtGui.QIcon('Images/teacher.svg')
    app.setWindowIcon(icon)

    #locale = QtCore.QLocale.system()
    #translator = QtCore.QTranslator()

    #i18n_file = '' + locale.name() + '.qm'
    #i18n_path = ''

    #if (translator.load(i18n_file, i18n_path)):
    #    app.installTranslator(translator)

    teacherView = TeacherView()
    teacherView.show()
    teacherView.login()
    app.exec_()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start()
