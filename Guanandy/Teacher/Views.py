from PySide2 import QtCore, QtGui, QtWidgets

from Guanandy.Protocol.Signals import protocolSignal
from Guanandy.Teacher.Models import StudentModel
from Guanandy.Broadcast import BroadcastServer
from Guanandy.Multicast import MulticastServer
from Guanandy import Util
from Guanandy import Controller
from Guanandy import getVersion


class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        self.setWindowTitle('Teacher Login')

        self.gridLayout = QtWidgets.QGridLayout(self)

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('Enter your name or class name')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.teacherName = QtWidgets.QLineEdit(self)
        self.teacherName.insert('Prof. Raimundo')
        self.gridLayout.addWidget(self.teacherName, 1, 0, 1, 1)

        self.errorMessage = QtWidgets.QLabel(self)
        self.errorMessage.clear()
        self.errorMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.errorMessage, 2, 0, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

    def closeEvent(self, event):
        """ To prevent the X button from close this dialog """
        event.ignore()

    def reject(self):
        """ To prevent the ESC key from close this dialog """
        pass

    def accept(self):
        """ Validate if teacher or classroom name is not empty """
        if self.teacherName.text() in Util.EMPTY_VALUES:
            self.errorMessage.setText('This field is required.')
        else:
            super(LoginDialog, self).accept()


class CloseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CloseDialog, self).__init__(parent)

        self.setWindowTitle('Close teacher')

        self.gridLayout = QtWidgets.QGridLayout(self)

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('Do you really want to quit?')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
                QtWidgets.QDialogButtonBox.Yes|QtWidgets.QDialogButtonBox.No)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)


class TeacherView(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TeacherView, self).__init__(parent)

        self.broadcastServer = None
        self.broadcastPort = 65535
        self.multicastServer = None
        self.multicastPort = 65532
        self.publisher = None
        self.publisherPort = 65534
        self.reply = None
        self.replyPort = 65533

        self.ip = None

        protocolSignal.callAttention.connect(self.callAttention)

        self.setWindowTitle('Guanandy Teacher')

        self.guanandy = QtWidgets.QWidget(self)

        self.studentModel = StudentModel(self.guanandy)

        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(
                self.guanandy.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(self.sizePolicy)

        self.guanandyLayout = QtWidgets.QGridLayout(self.guanandy)

        # Header layout
        self.headerLayout = QtWidgets.QHBoxLayout()
        self.guanandyLogo = QtWidgets.QLabel(self.guanandy)
        self.guanandyLogo.setText('')
        self.guanandyLogo.setPixmap(
                QtGui.QPixmap('Images/guanandy32x180.png'))
        self.headerLayout.addWidget(self.guanandyLogo)

        #self.headerSpacer = QtWidgets.QSpacerItem(40, 20,
        #        QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.headerLayout.addItem(self.headerSpacer)

        self.guanandyLayout.addLayout(self.headerLayout, 0, 0, 1, 1)

        # Commands layout
        self.commandsLayout = QtWidgets.QHBoxLayout()
        self.sendScreenButton = QtWidgets.QToolButton(self.guanandy)
        self.sendScreenIcon = QtGui.QIcon()
        self.sendScreenIcon.addPixmap(
                QtGui.QPixmap('Images/sendScreen.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sendScreenButton.setIcon(self.sendScreenIcon)
        self.sendScreenButton.setIconSize(QtCore.QSize(64, 64))
        self.sendScreenButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.sendScreenButton.setText('Send screen')
        self.commandsLayout.addWidget(self.sendScreenButton)

        self.lockScreensButton = QtWidgets.QToolButton(self.guanandy)
        self.lockScreensIcon = QtGui.QIcon()
        self.lockScreensIcon.addPixmap(
                QtGui.QPixmap('Images/lockScreen.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lockScreensButton.setIcon(self.lockScreensIcon)
        self.lockScreensButton.setIconSize(QtCore.QSize(64, 64))
        self.lockScreensButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.lockScreensButton.setText('Lock screen')
        self.commandsLayout.addWidget(self.lockScreensButton)

        self.shareFilesButton = QtWidgets.QToolButton(self.guanandy)
        self.shareFilesIcon = QtGui.QIcon()
        self.shareFilesIcon.addPixmap(
                QtGui.QPixmap('Images/shareFiles.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shareFilesButton.setIcon(self.shareFilesIcon)
        self.shareFilesButton.setIconSize(QtCore.QSize(64, 64))
        self.shareFilesButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.shareFilesButton.setText('Share files')
        self.shareFilesButton.clicked.connect(self.shareFile)
        self.commandsLayout.addWidget(self.shareFilesButton)

        self.shareWebPageButton = QtWidgets.QToolButton(self.guanandy)
        self.shareWebPageIcon = QtGui.QIcon()
        self.shareWebPageIcon.addPixmap(
                QtGui.QPixmap('Images/shareWebPage.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shareWebPageButton.setIcon(self.shareWebPageIcon)
        self.shareWebPageButton.setIconSize(QtCore.QSize(64, 64))
        self.shareWebPageButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.shareWebPageButton.setText('Share web page')
        self.commandsLayout.addWidget(self.shareWebPageButton)

        self.sendMessageButton = QtWidgets.QToolButton(self.guanandy)
        self.sendMessageIcon = QtGui.QIcon()
        self.sendMessageIcon.addPixmap(
                QtGui.QPixmap('Images/sendMessage.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sendMessageButton.setIcon(self.sendMessageIcon)
        self.sendMessageButton.setIconSize(QtCore.QSize(64, 64))
        self.sendMessageButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.sendMessageButton.setText('Send message')
        self.commandsLayout.addWidget(self.sendMessageButton)

        self.openApplicationButton = QtWidgets.QToolButton(self.guanandy)
        self.openApplicationIcon = QtGui.QIcon()
        self.openApplicationIcon.addPixmap(
                QtGui.QPixmap('Images/openApplication.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openApplicationButton.setIcon(self.openApplicationIcon)
        self.openApplicationButton.setIconSize(QtCore.QSize(64, 64))
        self.openApplicationButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.openApplicationButton.setText('Open application')
        self.commandsLayout.addWidget(self.openApplicationButton)

        self.turnOffStudentsButton = QtWidgets.QToolButton(self.guanandy)
        self.turnOffStudentsIcon = QtGui.QIcon()
        self.turnOffStudentsIcon.addPixmap(
                QtGui.QPixmap('Images/turnOffStudents.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.turnOffStudentsButton.setIcon(self.turnOffStudentsIcon)
        self.turnOffStudentsButton.setIconSize(QtCore.QSize(64, 64))
        self.turnOffStudentsButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.turnOffStudentsButton.setText('Turn off students')
        self.commandsLayout.addWidget(self.turnOffStudentsButton)
        self.guanandyLayout.addLayout(self.commandsLayout, 1, 0, 1, 1)

        # Students layout
        self.studentsLayout = QtWidgets.QVBoxLayout()
        self.studentListView = QtWidgets.QListView(self.guanandy)
        self.studentListView.setModel(self.studentModel)
        self.studentListView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.studentsLayout.addWidget(self.studentListView)
        self.guanandyLayout.addLayout(self.studentsLayout, 3, 0, 1, 1)

        # Footer layout
        self.footerLayout = QtWidgets.QHBoxLayout()

        self.historyButton = QtWidgets.QToolButton(self.guanandy)
        self.historyIcon = QtGui.QIcon()
        self.historyIcon.addPixmap(
                QtGui.QPixmap('Images/history.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.historyButton.setIcon(self.historyIcon)
        self.historyButton.setIconSize(QtCore.QSize(32, 32))
        self.historyButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextBesideIcon)
        self.historyButton.setText('History')
        self.footerLayout.addWidget(self.historyButton)

        self.footerLabel = QtWidgets.QLabel(self.guanandy)
        self.footerLabel.setText('Version:')
        self.footerLayout.addWidget(self.footerLabel)

        self.systemVersion = QtWidgets.QLabel(self.guanandy)
        self.systemVersion.setText(getVersion())
        self.footerLayout.addWidget(self.systemVersion)

        self.footerSpacer = QtWidgets.QSpacerItem(32, 32,
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.footerLayout.addItem(self.footerSpacer)

        self.exitSystemButton = QtWidgets.QToolButton(self.guanandy)
        self.exitSystemIcon = QtGui.QIcon()
        self.exitSystemIcon.addPixmap(
                QtGui.QPixmap('Images/exit.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitSystemButton.setIcon(self.exitSystemIcon)
        self.exitSystemButton.setIconSize(QtCore.QSize(32, 32))
        self.exitSystemButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextBesideIcon)
        self.exitSystemButton.setText('Exit')
        self.exitSystemButton.clicked.connect(self.close)
        self.footerLayout.addWidget(self.exitSystemButton)

        self.guanandyLayout.addLayout(self.footerLayout, 4, 0, 1, 1)
        self.setCentralWidget(self.guanandy)

    def login(self):
        loginDialog = LoginDialog(self)

        if loginDialog.exec_():
            teacherName = loginDialog.teacherName.text()

            self.broadcastServer = BroadcastServer('255.255.255.255',
                    self.broadcastPort, teacherName, self.publisherPort, parent=self)
            self.broadcastServer.start()

            self.ip = Util.ipAddress()

            self.publisher = Controller.Publisher(self.ip, self.publisherPort, parent=self)
            self.publisher.start()

            self.reply = Controller.Reply(self.ip, self.replyPort, parent=self)
            self.reply.start()

            self.multicastServer = MulticastServer(self.ip, self.multicastPort, parent=self)
            self.multicastServer.start()

    def shareFile(self):
        studentsIndex = self.studentListView.selectedIndexes()
        if studentsIndex not in Util.EMPTY_VALUES:
            fileName = QtWidgets.QFileDialog.getOpenFileName(self,
                    'Choose a file to share', Util.homeDirectory(), None)[0]
            if fileName not in Util.EMPTY_VALUES:
                for index in studentsIndex:
                    student = index.data(role=1111)
                    if student:
                        student.shareFile(fileName, self.multicastPort)
                    else:
                        print('No student selected')
            else:
                print('Share file canceled')
        else:
            QtWidgets.QMessageBox.warning(self, 'Select a student',
                    'You must select at least on student.')

    def callAttention(self, studentName):
        QtWidgets.QMessageBox.information(self, 'Student message',
                'Student {0} call attetion!'.format(studentName))

    def closeEvent(self, event):
        closeDialog = CloseDialog(self)
        if closeDialog.exec_():
            self.broadcastServer.stop()
            self.publisher.stop()
            self.reply.stop()
            event.accept()
        else:
            closeDialog.reject()
            event.ignore()

