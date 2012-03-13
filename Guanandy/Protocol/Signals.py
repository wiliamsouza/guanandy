from PySide import QtCore

class ProtocolSignal(QtCore.QObject):
    callAttention = QtCore.Signal()

protocolSignal = ProtocolSignal()
