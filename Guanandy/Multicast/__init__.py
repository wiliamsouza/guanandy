"""
Multicast server and client that use OpenPGM.

"""

import sys
import os
import time
import hashlib
import logging

import zmq

from PySide import QtCore

logger = logging.getLogger(__name__)


class MulticastServer(QtCore.QThread):
    """
    Multicast server
    """

    def __init__(self, ip, port, parent):
        QtCore.QThread.__init__(self, parent)
        self.running = False
        self.context = None
        self.message = None
        self.publisher = None
        self.filePath = None
        self.fileSize = None
        self.uri = 'epgm://%s;239.192.0.1:%s' % (ip, port)

    def run(self):
        logger.info('Starting multicast server on: %s' % self.uri)
        self.running = True
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)

        # Setting rate limit to 1Mbps
        #self.publisher.setsockopt(zmq.RATE, 1000)

        # Discard unsent messages on close
        #self.publisher.setsockopt(zmq.LINGER, 0)

        try:
            self.publisher.bind(self.uri)
        except:
            logger.critical('Multicast server bind error: {0}'.format(sys.exc_info()[1]))
            self.stop()

        #self.f = open(file_path, 'rb')
        #self.md5 = hashlib.md5()

        #self.total = 0
        while self.running:
            if self.message:
                #data = self.f.read(1436)
                #self.md5.update(data)
                self.publisher.send(self.message)
                logger.debug('Multicast server sent a message: %s' % self.message)
                self.message = None
                #total += 1436

                #if not data:
                #    self.stop()
            time.sleep(1)

    def send(message):
        self.message = message

    def stop(self):
        self.running = False
        #self.f.close()
        #print 'md5 checksum:', md5.hexdigest()
        self.wait()
        self.exit()

class MulticastClient(QtCore.QThread):
    """
    Multicast client
    """

    def __init__(self, filePath, ip, port, parent):
        QtCore.QThread.__init__(self, parent)
        self.running = False
        self.endpoint = 'epgm://%s;239.192.0.1:%s' % (ip, port)
        self.filePath = filePath

    def run(self):
        self.running = True
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect(self.endpoint)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, '')

        self.f = open(self.filePath, 'wb')

        while self.running:
            data = self.subscriber.recv()
            if not data:
                self.stop()
            self.f.write(data)
            time.sleep(1)

    def stop(self):
        self.running = False
        self.f.close()
        self.wait()
        self.exit()
