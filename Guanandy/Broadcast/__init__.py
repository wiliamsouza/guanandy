import time
import socket
import logging

from PySide import QtCore

from Guanandy.Broadcast.Signals import broadcastSignal

# TODO: may be implement time.sleep(random.randint(1, 5))

class BroadcastServer(QtCore.QThread):

    def __init__(self, ip, port, teacherName, teacherPort, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.running = False
        self.teacherName = teacherName
        self.teacherPort = str(teacherPort)
        self.message = '|'.join((self.teacherName, self.teacherPort))
        self.ip = ip
        self.port = port

    def run(self):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind(('', self.port))
        except socket.error, error:
            print 'Socket bind error:', error.message
            print 'Exiting...'
            self.wait()
            self.exit()

        while self.running:
            try:
                self.sock.sendto(self.message, (self.ip, self.port))
            except socket.error, error:
                print error
                continue
            time.sleep(1)

    def stop(self):
        self.running = False
        self.wait()
        self.exit()


class BroadcastClient(QtCore.QThread):

    def __init__(self, port, datagramSize, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.port = port
        self.datagramSize = datagramSize

    def run(self):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)

        try:
            self.sock.bind(('', self.port))
        except socket.error, error:
            print 'Socket bind error:', error.message
            print 'Exiting...'
            self.wait()
            self.exit()

        while self.running:
            try:
                message, (ip, port) = self.sock.recvfrom(self.datagramSize)
                teacherName, teacherPort = message.split('|')
                broadcastSignal.teacherFound.emit(teacherName, ip, teacherPort)
            except socket.timeout:
                pass
            time.sleep(1)

    def stop(self):
        self.running = False
        self.wait()
        self.exit()
