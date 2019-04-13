from PySide2 import QtCore

from Guanandy.Broadcast.Signals import broadcastSignal


class Teacher(QtCore.QObject):
    def __init__(self, name, ip, port, parent):
        super(Teacher, self).__init__(parent)
        self.__name = name
        self.__ip = ip
        self.__port = port

    def __getName(self):
        return str(self.__name)

    def __getIp(self):
        return str(self.__ip)

    def __getPort(self):
        return str(self.__port)

    changed = QtCore.Signal()
    name = QtCore.Property(str, __getName, notify=changed)
    ip = QtCore.Property(str, __getIp, notify=changed)
    port = QtCore.Property(str, __getPort, notify=changed)


class TeacherModel(QtCore.QAbstractListModel):

    def __init__(self, parent):
        super(TeacherModel, self).__init__(parent)
        self.__teachers = []
        broadcastSignal.teacherFound.connect(self.add)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__teachers)

    def data(self, index, role=QtCore.Qt.DisplayRole):

        # This role return teacher or classroom name
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return self.__teachers[index.row()].name

        # This role return teacher or classroom object instance
        if index.isValid() and role == 1111:
            return self.__teachers[index.row()]

        return None

    def add(self, name, ip, port):
        for t in self.__teachers:
            if t.name == name:
                return
        self.beginInsertRows(QtCore.QModelIndex(), len(self.__teachers),
                len(self.__teachers))
        teacher = Teacher(name, ip, port, self)
        self.__teachers.append(teacher)
        self.endInsertRows()
