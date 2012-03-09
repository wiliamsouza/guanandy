import os
import hashlib

import zmq

from PySide import QtCore

class MulticastServer(QtCore.QThread):

    def __init__(self, filePath, ip, port=5555, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.running = False
        self.endpoint = 'epgm://%s;239.192.0.1:%s' % (ip, port)
        self.filePath = filePath
        self.fileSize = os.path.getsize(self.ilePath)

    def run(self):
        self.running = True
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)

        # Setting rate limit to 1Mbps
        #self.publisher.setsockopt(zmq.RATE, 1000)

        # Discard unsent messages on close
        #self.publisher.setsockopt(zmq.LINGER, 0)

        self.publisher.bind(self.endpoint)

        self.f = open(file_path, 'rb')

        self.md5 = hashlib.md5()

        self.total = 0
        while self.running:
            data = self.f.read(1436)
            self.md5.update(data)
            self.publisher.send(data)
            total += 1436

            if not data:
                self.stop()

    def stop(self):
        self.running = False
        self.f.close()
        print 'md5 checksum:', md5.hexdigest()
        self.wait()
        self.exit()

class MulticastClient(QtCore.QThread):

    def __init__(self, filePath, ip, port=5555, parent=None):
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
