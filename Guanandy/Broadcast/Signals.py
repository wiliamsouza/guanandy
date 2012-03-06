from PySide import QtCore

class BroadcastSignal(QtCore.QObject):
    classroomFound = QtCore.Signal(str, str)

broadcastSignal = BroadcastSignal()
