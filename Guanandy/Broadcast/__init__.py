"""
Broadcast server and client, teacher discovery is done using it.

"""

import time
import socket
import logging

from PySide2 import QtCore

from Guanandy.Broadcast.Signals import broadcastSignal

logger = logging.getLogger(__name__)


class BroadcastServer(QtCore.QThread):

    def __init__(self, ip, port, teacherName, teacherPort, parent):
        QtCore.QThread.__init__(self, parent)
        self.running = False
        self.sock = None
        self.teacherName = teacherName
        self.teacherPort = str(teacherPort)
        self.message = '|'.join((self.teacherName, self.teacherPort))
        self.ip = ip
        self.port = port

    def run(self):
        logger.info('Starting server on: %s, %d' % (self.ip, self.port))
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind(('', self.port))
        except socket.error as error:
            logger.critical('socker.bind error: %s' % error)
            self.stop()

        while self.running:
            try:
                self.sock.sendto(bytes(self.message, 'utf-8'), (self.ip, self.port))
                logger.debug('Message sent: %s' % self.message)
            except socket.error as error:
                logger.error('socket.sendto error: %s' % error)
            time.sleep(1)

    def stop(self):
        logger.info('Stopping server')
        self.running = False
        self.sock.close()
        self.wait()
        self.exit()


class BroadcastClient(QtCore.QThread):
    """

    """

    def __init__(self, port, datagramSize, parent):
        QtCore.QThread.__init__(self, parent)
        self.port = port
        self.datagramSize = datagramSize

    def run(self):
        logger.info('Starting client on: %d' % self.port)
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)

        try:
            self.sock.bind(('', self.port))
        except socket.error as error:
            logger.critical('socket.bind error: %s' % error)
            self.stop()

        while self.running:
            try:
                message, (ip, port) = self.sock.recvfrom(self.datagramSize)
                teacherName, teacherPort = message.split(b'|')
                logger.debug('Message received: %s' % message)
                broadcastSignal.teacherFound.emit(teacherName, ip, teacherPort)
            except socket.timeout as error:
                logger.debug('Message timeout: %s', error)
            time.sleep(1)

    def stop(self):
        logger.debug('Stopping client')
        self.running = False
        self.sock.close()
        self.wait()
        self.exit()
