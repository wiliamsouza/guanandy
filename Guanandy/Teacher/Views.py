from PySide import QtCore, QtGui, QtUiTools

from Classroom.Broadcast import BroadcastServer
from Classroom.Util import EMPTY_VALUES

class LoginDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        #QtGui.QDialog.__init__(self, parent)
        super(LoginDialog, self).__init__(parent)

        self.setWindowTitle('Classroom Login')

        self.gridLayout = QtGui.QGridLayout(self)

        self.label = QtGui.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('Enter your name or class name')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.classroomName= QtGui.QLineEdit(self)
        self.gridLayout.addWidget(self.classroomName, 1, 0, 1, 1)

        self.errorMessage = QtGui.QLabel(self)
        self.errorMessage.setText('Error Message')
        self.errorMessage.clear()
        self.errorMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.errorMessage, 2, 0, 1, 1)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

    def closeEvent(self, event):
        """ To prevent the X button from close this dialog """
        event.ignore()

    def reject(self):
        """ To prevent the ESC key from close this dialog """
        pass

    def accept(self):
        """ Validate if classroom name is not empty """
        if self.classroomName.text() in EMPTY_VALUES:
            self.errorMessage.setText('This field is required.')
        else:
            #QtGui.QDialog.accept(self)
            super(LoginDialog, self).accept()


class CloseDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        #QtGui.QDialog.__init__(self, parent)
        super(CloseDialog, self).__init__(parent)

        self.setWindowTitle('Close ClassRoom')

        self.gridLayout = QtGui.QGridLayout(self)

        self.label = QtGui.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('Do you really want to quit?')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
                QtGui.QDialogButtonBox.Yes|QtGui.QDialogButtonBox.No)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)


class ClassRoomView(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #QtGui.QMainWindow.__init__(self, parent)
        super(ClassRoomView, self).__init__(parent)

        self.setWindowTitle('ClassRoom Teacher')

        self.classroom = QtGui.QWidget(self)

        self.sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(
                self.classroom.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(self.sizePolicy)

        self.classroomLayout = QtGui.QGridLayout(self.classroom)

        # Header layout
        self.headerLayout = QtGui.QHBoxLayout()
        self.classroomLogo = QtGui.QLabel(self.classroom)
        self.classroomLogo.setText('')
        self.classroomLogo.setPixmap(
                QtGui.QPixmap('Images/classroom.png'))
        self.headerLayout.addWidget(self.classroomLogo)

        #self.headerSpacer = QtGui.QSpacerItem(40, 20,
        #        QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        #self.headerLayout.addItem(self.headerSpacer)

        self.classroomLayout.addLayout(self.headerLayout, 0, 0, 1, 1)

        # Commands layout
        self.commandsLayout = QtGui.QHBoxLayout()
        self.sendScreenButton = QtGui.QToolButton(self.classroom)
        self.sendScreenIcon = QtGui.QIcon()
        self.sendScreenIcon.addPixmap(
                QtGui.QPixmap('Images/sendScreen.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sendScreenButton.setIcon(self.sendScreenIcon)
        self.sendScreenButton.setIconSize(QtCore.QSize(60, 55))
        self.sendScreenButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.sendScreenButton.setText('Send screen')
        self.commandsLayout.addWidget(self.sendScreenButton)

        self.lockScreensButton = QtGui.QToolButton(self.classroom)
        self.lockScreensIcon = QtGui.QIcon()
        self.lockScreensIcon.addPixmap(
                QtGui.QPixmap('Images/lockScreens.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lockScreensButton.setIcon(self.lockScreensIcon)
        self.lockScreensButton.setIconSize(QtCore.QSize(60, 55))
        self.lockScreensButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.lockScreensButton.setText('Lock screens')
        self.commandsLayout.addWidget(self.lockScreensButton)

        self.shareFilesButton = QtGui.QToolButton(self.classroom)
        self.shareFilesIcon = QtGui.QIcon()
        self.shareFilesIcon.addPixmap(
                QtGui.QPixmap('Images/shareFiles.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shareFilesButton.setIcon(self.shareFilesIcon)
        self.shareFilesButton.setIconSize(QtCore.QSize(60, 55))
        self.shareFilesButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.shareFilesButton.setText('Share files')
        self.commandsLayout.addWidget(self.shareFilesButton)

        self.shareWebPageButton = QtGui.QToolButton(self.classroom)
        self.shareWebPageIcon = QtGui.QIcon()
        self.shareWebPageIcon.addPixmap(
                QtGui.QPixmap('Images/shareWebPage.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shareWebPageButton.setIcon(self.shareWebPageIcon)
        self.shareWebPageButton.setIconSize(QtCore.QSize(60, 55))
        self.shareWebPageButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.shareWebPageButton.setText('Share web page')
        self.commandsLayout.addWidget(self.shareWebPageButton)

        self.sendMessageButton = QtGui.QToolButton(self.classroom)
        self.sendMessageIcon = QtGui.QIcon()
        self.sendMessageIcon.addPixmap(
                QtGui.QPixmap('Images/sendMessage.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sendMessageButton.setIcon(self.sendMessageIcon)
        self.sendMessageButton.setIconSize(QtCore.QSize(60, 55))
        self.sendMessageButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.sendMessageButton.setText('Send message')
        self.commandsLayout.addWidget(self.sendMessageButton)

        self.openApplicationButton = QtGui.QToolButton(self.classroom)
        self.openApplicationIcon = QtGui.QIcon()
        self.openApplicationIcon.addPixmap(
                QtGui.QPixmap('Images/openApplication.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openApplicationButton.setIcon(self.openApplicationIcon)
        self.openApplicationButton.setIconSize(QtCore.QSize(60, 55))
        self.openApplicationButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.openApplicationButton.setText('Open application')
        self.commandsLayout.addWidget(self.openApplicationButton)

        self.turnOffStudentsButton = QtGui.QToolButton(self.classroom)
        self.turnOffStudentsIcon = QtGui.QIcon()
        self.turnOffStudentsIcon.addPixmap(
                QtGui.QPixmap('Images/turnOffStudents.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.turnOffStudentsButton.setIcon(self.turnOffStudentsIcon)
        self.turnOffStudentsButton.setIconSize(QtCore.QSize(60, 55))
        self.turnOffStudentsButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.turnOffStudentsButton.setText('Turn off students')
        self.commandsLayout.addWidget(self.turnOffStudentsButton)
        self.classroomLayout.addLayout(self.commandsLayout, 1, 0, 1, 1)

        # Students layout
        self.studentsLayout = QtGui.QVBoxLayout()
        self.studentListView = QtGui.QListView(self.classroom)
        self.studentsLayout.addWidget(self.studentListView)
        self.classroomLayout.addLayout(self.studentsLayout, 3, 0, 1, 1)

        # Footer layout
        self.footerLayout = QtGui.QHBoxLayout()
        self.footerLabel = QtGui.QLabel(self.classroom)
        self.footerLabel.setText('System version:')
        self.footerLayout.addWidget(self.footerLabel)

        self.systemVersion = QtGui.QLabel(self.classroom)
        self.systemVersion.setText('0.0-0')
        self.footerLayout.addWidget(self.systemVersion)

        self.historyButton = QtGui.QPushButton(self.classroom)
        self.historyButton.setText('History')
        self.footerLayout.addWidget(self.historyButton)

        self.footerSpacer = QtGui.QSpacerItem(40, 20,
                QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.footerLayout.addItem(self.footerSpacer)

        self.exitSystemButton = QtGui.QToolButton(self.classroom)
        self.exitSystemButton.setText('Exit system')
        self.exitSystemButton.clicked.connect(self.close)
        self.footerLayout.addWidget(self.exitSystemButton)

        self.classroomLayout.addLayout(self.footerLayout, 4, 0, 1, 1)
        self.setCentralWidget(self.classroom)

    def login(self):
        loginDialog = LoginDialog(self)
        if loginDialog.exec_():
            classroomName = loginDialog.classroomName.text()
            self.broadcastServer = BroadcastServer('255.255.255.255',
                    65535,
                    classroomName,
                    parent= self)
            self.broadcastServer.start()

    def closeEvent(self, event):
        closeDialog = CloseDialog(self)
        if closeDialog.exec_():
            self.broadcastServer.stop()
            event.accept()
        else:
            closeDialog.reject()
            event.ignore()

