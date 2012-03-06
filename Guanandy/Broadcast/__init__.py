import time
import socket
import logging

from PySide import QtCore

from Guanandy.Broadcast.Signals import broadcastSignal

class BroadcastServer(QtCore.QThread):

    def __init__(self, ip, port, message, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.running = False
        self.message = message
        self.ip = ip
        self.port = port

    def run(self):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind(('', 0))
        except socket.error, error:
            print 'Socket bind error:', error.message
            print 'Exiting...'
            self.wait()
            self.exit()

        while self.running:
            self.sock.sendto(self.message, (self.ip, self.port))
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
            self.sock.bind(('', 0))
        except socket.error, error:
            print 'Socket bind error:', error.message
            print 'Exiting...'
            self.wait()
            self.exit()

        while self.running:
            try:
                message, (ip, port) = self.sock.recvfrom(self.datagramSize)
                broadcastSignal.teacherFound.emit(message, ip)
            except socket.timeout:
                pass
            time.sleep(1)

    def stop(self):
        self.running = False
        self.wait()
        self.exit()
