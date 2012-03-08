from PySide import QtCore, QtGui, QtUiTools

from Guanandy.Broadcast import BroadcastServer
from Guanandy.Util import EMPTY_VALUES

class LoginDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        #QtGui.QDialog.__init__(self, parent)
        super(LoginDialog, self).__init__(parent)

        self.setWindowTitle('Teacher Login')

        self.gridLayout = QtGui.QGridLayout(self)

        self.label = QtGui.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('Enter your name or class name')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.teacherName= QtGui.QLineEdit(self)
        self.gridLayout.addWidget(self.teacherName, 1, 0, 1, 1)

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
        """ Validate if guanandy name is not empty """
        if self.teacherName.text() in EMPTY_VALUES:
            self.errorMessage.setText('This field is required.')
        else:
            #QtGui.QDialog.accept(self)
            super(LoginDialog, self).accept()


class CloseDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        #QtGui.QDialog.__init__(self, parent)
        super(CloseDialog, self).__init__(parent)

        self.setWindowTitle('Close teacher')

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


class TeacherView(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #QtGui.QMainWindow.__init__(self, parent)
        super(TeacherView, self).__init__(parent)

        self.setWindowTitle('Guanandy Teacher')

        self.guanandy = QtGui.QWidget(self)

        self.sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(
                self.guanandy.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(self.sizePolicy)

        self.guanandyLayout = QtGui.QGridLayout(self.guanandy)

        # Header layout
        self.headerLayout = QtGui.QHBoxLayout()
        self.guanandyLogo = QtGui.QLabel(self.guanandy)
        self.guanandyLogo.setText('')
        self.guanandyLogo.setPixmap(
                QtGui.QPixmap('Images/guanandy32x180.png'))
        self.headerLayout.addWidget(self.guanandyLogo)

        #self.headerSpacer = QtGui.QSpacerItem(40, 20,
        #        QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        #self.headerLayout.addItem(self.headerSpacer)

        self.guanandyLayout.addLayout(self.headerLayout, 0, 0, 1, 1)

        # Commands layout
        self.commandsLayout = QtGui.QHBoxLayout()
        self.sendScreenButton = QtGui.QToolButton(self.guanandy)
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

        self.lockScreensButton = QtGui.QToolButton(self.guanandy)
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

        self.shareFilesButton = QtGui.QToolButton(self.guanandy)
        self.shareFilesIcon = QtGui.QIcon()
        self.shareFilesIcon.addPixmap(
                QtGui.QPixmap('Images/shareFiles.png'),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shareFilesButton.setIcon(self.shareFilesIcon)
        self.shareFilesButton.setIconSize(QtCore.QSize(64, 64))
        self.shareFilesButton.setToolButtonStyle(
                QtCore.Qt.ToolButtonTextUnderIcon)
        self.shareFilesButton.setText('Share files')
        self.commandsLayout.addWidget(self.shareFilesButton)

        self.shareWebPageButton = QtGui.QToolButton(self.guanandy)
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

        self.sendMessageButton = QtGui.QToolButton(self.guanandy)
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

        self.openApplicationButton = QtGui.QToolButton(self.guanandy)
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

        self.turnOffStudentsButton = QtGui.QToolButton(self.guanandy)
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
        self.studentsLayout = QtGui.QVBoxLayout()
        self.studentListView = QtGui.QListView(self.guanandy)
        self.studentsLayout.addWidget(self.studentListView)
        self.guanandyLayout.addLayout(self.studentsLayout, 3, 0, 1, 1)

        # Footer layout
        self.footerLayout = QtGui.QHBoxLayout()

        self.historyButton = QtGui.QToolButton(self.guanandy)
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

        self.footerLabel = QtGui.QLabel(self.guanandy)
        self.footerLabel.setText('Version:')
        self.footerLayout.addWidget(self.footerLabel)

        self.systemVersion = QtGui.QLabel(self.guanandy)
        self.systemVersion.setText('2.0')
        self.footerLayout.addWidget(self.systemVersion)

        self.footerSpacer = QtGui.QSpacerItem(32, 32,
                QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.footerLayout.addItem(self.footerSpacer)

        self.exitSystemButton = QtGui.QToolButton(self.guanandy)
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
                    65535,
                    teacherName,
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

