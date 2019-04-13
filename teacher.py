#!/usr/bin/env python

import sys
import logging

from PySide2 import QtGui, QtWidgets

from Guanandy.Teacher.Views import TeacherView


def start():

    app = QtWidgets.QApplication(sys.argv)

    icon = QtGui.QIcon('Images/teacher.svg')
    app.setWindowIcon(icon)

    teacherView = TeacherView()
    teacherView.show()
    teacherView.login()
    app.exec_()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start()
