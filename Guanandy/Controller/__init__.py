import os
import hashlib

import zmq

from PySide import QtCore


class Publisher(QtCore.QThread):

    def __init__(self, ip, port, parent=None):
        super(Publisher, self).__init__(parent)
        self.running = False
        self.context = None
        self.message = None
        self.publisher = None
        self.uri = 'tcp://%s:%s' % (ip, port)

    def run(self):
        self.running = True
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)

        # Setting rate limit to 1Mbps
        #self.publisher.setsockopt(zmq.RATE, 1000)

        # Discard unsent messages on close
        #self.publisher.setsockopt(zmq.LINGER, 0)

        self.publisher.bind(self.uri)

        while self.running:
            if self.message:
                self.publisher.send(self.message)
                self.message = None

    def send(message):
        self.message = message

    def stop(self):
        self.running = False
        self.publisher.close()
        self.context.term()
        self.wait()
        self.exit()


class Subscriber(QtCore.QThread):

    def __init__(self, ip, port, name, parent=None):
        super(Subscriber, self).__init__(parent)
        self.running = False
        self.context = None
        self.message = None
        self.subscribe = None
        self.name = name
        self.uri = 'tcp://%s:%s' % (ip, port)

    def run(self):
        self.running = True
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect(self.uri)
        self.subscriber.setsockopt(zmq.SUBSCRIBE, self.name)

        while self.running:
            self.message = self.subscriber.recv()

    def stop(self):
        self.running = False
        self.subscriber.close()
        self.context.term()
        self.wait()
        self.exit()


class Client(QtCore.QThread):

    def __init__(self, ip, port, parent=None):
        super(Client, self).__init__(parent)
        self.running = False
        self.uri = 'tcp://%s:%s' % (ip, port)
        self.message = None

    def run(self):
        print 'starting'
        self.running = True

        self.context = zmq.Context()
        self.request = self.context.socket(zmq.REQ)
        self.request.connect(self.uri)

        while self.running:
            if self.message:
                print 'Sending: ', self.message
                self.request.send(self.message)

                print 'Waiting response...'
                self.response = self.request.recv()
                print 'Received response: ', self.response
                self.message = None

    def send(self, message):
        self.message = message

    def stop(self):
        self.running = False
        self.request.close()
        self.context.term()
        self.wait()
        self.exit()


class Server(QtCore.QThread):

    def __init__(self, ip, port, parent=None):
        super(Server, self).__init__(parent)
        self.running = False
        self.uri = 'tcp://%s:%s' % (ip, port)

    def run(self):
        self.running = True
        self.context = zmq.Context()
        self.response = self.context.socket(zmq.REP)
        self.response.bind(self.uri)

        msg = ''
        while self.running:
            print 'Waiting request...'
            self.request = self.response.recv()
            print 'Received: ', self.request
            print 'Sending: ', msg
            self.reponse.send(msg)

    def stop(self):
        self.running = False
        self.request.close()
        self.context.term()
        self.wait()
        self.exit()
