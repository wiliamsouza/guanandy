"""
Signal used for broadcast.

"""

from PySide2 import QtCore

class BroadcastSignal(QtCore.QObject):
    teacherFound = QtCore.Signal(str, str, str)

broadcastSignal = BroadcastSignal()
