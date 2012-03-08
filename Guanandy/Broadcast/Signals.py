from PySide import QtCore

class BroadcastSignal(QtCore.QObject):
    teacherFound = QtCore.Signal(str, str, str)

broadcastSignal = BroadcastSignal()
