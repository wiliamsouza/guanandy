from PySide import QtCore

class ProtocolSignal(QtCore.QObject):
    callAttention = QtCore.Signal(str)
    registerStudent = QtCore.Signal(str)

protocolSignal = ProtocolSignal()
