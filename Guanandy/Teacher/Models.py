from PySide import QtCore

from Guanandy.Protocol.Signals import protocolSignal


class Student(QtCore.QObject):
    def __init__(self, name, parent=None):
        super(Student, self).__init__(parent)
        self.__name = name

    def __getName(self):
        return str(self.__name)

    changed = QtCore.Signal()
    name = QtCore.Property(unicode, __getName, notify=changed)


class StudentModel(QtCore.QAbstractListModel):

    def __init__(self, parent=None):
        super(StudentModel, self).__init__(parent)
        self.__students = []
        protocolSignal.registerStudent.connect(self.add)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__students)

    def data(self, index, role=QtCore.Qt.DisplayRole):

        # This role return student name
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return self.__students[index.row()].name

        # This role return student object instance
        if index.isValid() and role == 1111:
            return self.__students[index.row()]

        return None

    def add(self, name):
        for s in self.__students:
            if s.name == name:
                # TODO: Return a user exist error
                return
        self.beginInsertRows(QtCore.QModelIndex(), len(self.__students),
                len(self.__students))
        student = Student(name, self)
        self.__students.append(student)
        self.endInsertRows()
