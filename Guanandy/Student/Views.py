from PySide2 import QtCore, QtWidgets, QtGui

from Guanandy import Controller
from Guanandy.Util import EMPTY_VALUES
from Guanandy.Broadcast import BroadcastClient
from Guanandy.Student.Models import TeacherModel
from Guanandy.Protocol.Signals import protocolSignal


class StudentView(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(StudentView, self).__init__(parent)

        # Start broadcast client
        self.broadcastClient = BroadcastClient(65535, 255, parent=self)
        self.broadcastClient.start()

        # Attribute definition
        self.teacher = None
        self.subscriber = None
        self.request = None

        # Signals
        protocolSignal.shareFile.connect(self.shareFile)

        # Teacher model
        self.teacherModel = TeacherModel(self)

        # View definition
        self.setWindowTitle('Student Login')
        self.gridLayout = QtWidgets.QGridLayout(self)

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('Enter your name')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.studentName= QtWidgets.QLineEdit(self)
        self.studentName.insert('Seu Buneco')
        self.gridLayout.addWidget(self.studentName, 1, 0, 1, 1)

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setText('Select a teacher name or class name')
        self.gridLayout.addWidget(self.label1, 2, 0, 1, 1)

        self.teacherListView = QtWidgets.QListView(self)
        self.teacherListView.setModel(self.teacherModel)
        self.gridLayout.addWidget(self.teacherListView, 3, 0, 1, 1)

        self.errorMessage = QtWidgets.QLabel(self)
        self.errorMessage.setText('Error Message')
        self.errorMessage.clear()
        self.errorMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.errorMessage, 4, 0, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
                QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.connect)
        self.buttonBox.rejected.connect(self.hide)
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)

        # System tray actions
        self.loginAction = QtWidgets.QAction('&Login',
                self, triggered=self.show)
        self.logoutAction = QtWidgets.QAction('&Disconnect from',
                self, triggered=self.logout)
        self.callAttentionAction = QtWidgets.QAction('&Call attention',
                self, triggered=self.callAttention)
        self.downloadProgressAction = QtWidgets.QAction('Download &progress',
                self, triggered=self.downloadProgress)
        self.historyAction = QtWidgets.QAction('&History', self,
                triggered=self.history)
        self.aboutAction = QtWidgets.QAction('&About', self,
                triggered=self.about)
        self.quitAction = QtWidgets.QAction('&Quit', self, triggered=self.close)

        # System tray menu
        self.trayIconMenu = QtWidgets.QMenu(self)
        self.trayIconMenu.addAction(self.loginAction)
        self.trayIconMenu.addAction(self.logoutAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.callAttentionAction)
        self.trayIconMenu.addAction(self.downloadProgressAction)
        self.trayIconMenu.addAction(self.historyAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.aboutAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.sysTrayIcon = QtWidgets.QSystemTrayIcon(self)
        self.sysTrayIcon.setContextMenu(self.trayIconMenu)
        self.icon = QtGui.QIcon('Images/teacher22x22.png')
        self.sysTrayIcon.setIcon(self.icon)
        self.sysTrayIcon.setToolTip('Student')
        self.sysTrayIcon.show()

    def logout(self):
        pass

    def downloadProgress(self):
        pass

    def history(self):
        pass

    def about(self):
        pass

    def callAttention(self):
        if self.teacher:
            protocolSignal.callAttention.emit(self.studentName.text())

    def shareFile(self, fileName, multicastIp, multicastPort):
        print('Teacher want to share {0} with you'.format(fileName))

    def connect(self):
        studentName = self.studentName.text()

        if studentName in EMPTY_VALUES:
            self.errorMessage.setText('This field is required.')
            return

        # Get the current selected teacher
        teacherModel =  self.teacherListView.currentIndex()
        self.teacher =  teacherModel.data(role=1111)
        if self.teacher:
            self.subscriber = Controller.Subscriber(self.teacher.ip, self.teacher.port, studentName, parent=self)
            self.subscriber.start()

            self.request = Controller.Request(self.teacher.ip, 65533, parent=self)
            self.request.start()

            protocolSignal.registerStudent.emit(studentName)

            self.hide()
        else:
            self.errorMessage.setText('You must select one teacher.')

    def close(self):
        self.sysTrayIcon.hide()
        super(StudentView, self).close()

    def closeEvent(self, event):
        """ To prevent the window X button from close the application

        The closing event will be accepted only when fired from systray
        quit button.
        """
        if self.sysTrayIcon.isVisible():
            self.hide()
            event.ignore()
        else:
            QtWidgets.qApp.setQuitOnLastWindowClosed(True)
            self.broadcastClient.stop()
            self.subscriber.stop()
            self.request.stop()
            event.accept()
