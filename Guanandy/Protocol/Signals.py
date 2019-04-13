"""
Signals used for protocol module.
"""

from PySide2 import QtCore


class ProtocolSignal(QtCore.QObject):
    callAttention = QtCore.Signal(str)
    registerStudent = QtCore.Signal(str)
    shareFile = QtCore.Signal(str, str, str)

protocolSignal = ProtocolSignal()
