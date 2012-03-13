from PySide import QtCore, QtGui, QtUiTools

from Guanandy.Protocol.Signals import protocolSignal
from Guanandy.Student.Models import TeacherModel
from Guanandy.Broadcast import BroadcastClient
from Guanandy.Util import EMPTY_VALUES
from Guanandy import Controller


class StudentView(QtGui.QWidget):

    def __init__(self, parent=None):
        super(StudentView, self).__init__(parent)

        # Start broadcast client
        self.broadcastClient = BroadcastClient(65535, 255, parent=self)
        self.broadcastClient.start()

        self.subscriber = None
        self.request = None

        # Dialog
        self.setWindowTitle('Student Login')

        self.gridLayout = QtGui.QGridLayout(self)

        self.label = QtGui.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('Enter your name')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.studentName= QtGui.QLineEdit(self)
        self.gridLayout.addWidget(self.studentName, 1, 0, 1, 1)

        self.label1 = QtGui.QLabel(self)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setText('Select a teacher name or class name')
        self.gridLayout.addWidget(self.label1, 2, 0, 1, 1)

        # Model
        teacherModel = TeacherModel(self)

        self.teacherListView = QtGui.QListView(self)
        #self.teacherListView = QtGui.QTreeView(self)
        self.teacherListView.setModel(teacherModel)
        self.gridLayout.addWidget(self.teacherListView, 3, 0, 1, 1)

        self.errorMessage = QtGui.QLabel(self)
        self.errorMessage.setText('Error Message')
        self.errorMessage.clear()
        self.errorMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.errorMessage, 4, 0, 1, 1)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
                QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.connect)
        self.buttonBox.rejected.connect(self.hide)
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)

        # System tray actions
        self.loginAction = QtGui.QAction('&Login',
                self, triggered=self.login)
        self.logoutAction = QtGui.QAction('&Disconnect from',
                self, triggered=self.logout)
        self.callAttentionAction = QtGui.QAction('&Call attention',
                self, triggered=self.callAttention)
        self.downloadProgressAction = QtGui.QAction('Download &progress',
                self, triggered=self.downloadProgress)
        self.historyAction = QtGui.QAction('&History', self,
                triggered=self.history)
        self.aboutAction = QtGui.QAction('&About', self,
                triggered=self.about)
        self.quitAction = QtGui.QAction('&Quit', self, triggered=self.close)

        # System tray menu
        self.trayIconMenu = QtGui.QMenu(self)
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

        self.sysTrayIcon = QtGui.QSystemTrayIcon(self)
        self.sysTrayIcon.setContextMenu(self.trayIconMenu)
        self.icon = QtGui.QIcon('Images/teacher22x22.png')
        self.sysTrayIcon.setIcon(self.icon)
        self.sysTrayIcon.setToolTip('Student')
        self.sysTrayIcon.show()

    def login(self):
        self.show()

    def logout(self):
        pass

    def callAttention(self):
        protocolSignal.callAttention.emit()

    def downloadProgress(self):
        pass

    def history(self):
        pass

    def about(self):
        pass

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
            self.broadcastClient.stop()
            self.subscriber.stop()
            self.request.stop()
            QtGui.qApp.setQuitOnLastWindowClosed(True)
            event.accept()

    def connect(self):
        if self.studentName.text() in EMPTY_VALUES:
            self.errorMessage.setText('This field is required.')
            return

        # Get the current selected teacher or classroom
        teacherModel =  self.teacherListView.currentIndex()
        teacher =  teacherModel.data(role=1111)

        if not teacher:
            self.errorMessage.setText('You must select at least one teacher.')
        else:
            self.subscriber = Controller.Subscriber(teacher.ip, teacher.port, self.studentName.text())
            self.subscriber.start()

            self.request = Controller.Request(teacher.ip, 65533)
            self.request.start()

            self.hide()
