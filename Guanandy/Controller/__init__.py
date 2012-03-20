"""
This module contains server and client used to exchange messages from/to
teacher/student.

"""

import os
import sys
import time
import logging

import zmq

from PySide import QtCore

from Guanandy.Protocol.Signals import protocolSignal
from Guanandy import Protocol

logger = logging.getLogger(__name__)


class Publisher(QtCore.QThread):
    """
    A server that publishes messages to students.
    """

    def __init__(self, ip, port, parent):
        super(Publisher, self).__init__(parent)
        self.running = False
        self.context = None
        self.message = None
        self.publisher = None
        self.ip = ip
        self.port = port
        self.uri = 'tcp://%s:%s' % (self.ip, self.port)

    def run(self):
        logger.info('Starting publisher on: %s' % self.uri)
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
            logger.critical('Publisher bind error: {0}'.format(sys.exc_info()[1]))
            self.stop()

        while self.running:
            if self.message:
                self.publisher.send_json(self.message)
                logger.debug('Publisher sent a message: %s' % self.message)
                self.message = None
            time.sleep(1)

    def shareFile(self, fileName, multicastPort):
        protocol = Protocol.shareFile.copy()
        protocol['file'] = fileName
        protocol['ip'] = self.ip
        protocol['port'] = multicastPort
        self.send(protocol)

    def send(self, message):
        self.message = message

    def stop(self):
        logger.info('Stopping publisher')
        self.running = False
        self.publisher.close()
        self.context.term()
        self.wait()
        self.exit()


class Subscriber(QtCore.QThread):
    """
    A Client that receive published messages from teachers.
    """

    def __init__(self, ip, port, name, parent):
        super(Subscriber, self).__init__(parent)
        self.running = False
        self.context = None
        self.message = None
        self.subscribe = None
        self.name = name
        self.uri = 'tcp://%s:%s' % (ip, port)

    def run(self):
        logger.info('Starting subscriber on: %s' % self.uri)
        self.running = True
        self.context = zmq.Context()
        self.subscriber = self.context.socket(zmq.SUB)

        try:
            self.subscriber.connect(self.uri)
        except:
            logger.critical('Subscriber connect error: %s' % error)

        self.subscriber.setsockopt_unicode(zmq.SUBSCRIBE, u'')#self.name)

        while self.running:
            logger.debug('Subscriber waiting request...')
            request = self.subscriber.recv_json()
            logger.debug('Subscriber received request. %s' % request)

            try:
                getattr(self, request['action'])(request)
            except AttributeError, error:
                logger.warning('Subscriber received a bad request.')

    def shareFile(self, request):
        fileName = request['file']
        multicastIp = request['ip']
        multicastPort = request['port']
        protocolSignal.shareFile.emit(fileName, multicastIp, multicastPort)

    def stop(self):
        logger.info('Stopping subscriber')
        self.running = False
        self.subscriber.close()
        self.context.term()
        self.wait()
        self.exit()


class Request(QtCore.QThread):
    """
    A client used to talk with the teacher
    """

    def __init__(self, ip, port, parent):
        super(Request, self).__init__(parent)
        self.running = False
        self.uri = 'tcp://%s:%s' % (ip, port)
        self.message = None
        protocolSignal.callAttention.connect(self.callAttention)

    def run(self):
        logger.info('Starting request on: %s' % self.uri)
        self.running = True

        self.context = zmq.Context()
        self.request = self.context.socket(zmq.REQ)

        try:
            self.request.connect(self.uri)
        except:
            logger.critical('Request connect error: %s' % error)


        while self.running:
            if self.message:
                logger.debug('Request sending: %s' % self.message)
                self.request.send_json(self.message)

                logger.debug('Request waiting response...')
                self.response = self.request.recv_json()

                logger.debug('Request received response: %s' % \
                        self.response)
                self.message = None

            time.sleep(1)

    def registerStudent(self, studentName):
        protocol = Protocol.registerStudent.copy()
        protocol['studentName'] = studentName
        self.send(protocol)

    def callAttention(self, studentName):
        protocol = Protocol.callAttention.copy()
        protocol['studentName'] = studentName
        self.send(protocol)

    def send(self, message):
        self.message = message

    def stop(self):
        logger.info('Stopping request')
        self.running = False
        self.request.close()
        self.context.term()
        self.wait()
        self.exit()


class Reply(QtCore.QThread):
    """
    A server that listen for student request.
    """

    def __init__(self, ip, port, parent):
        super(Reply, self).__init__(parent)
        self.running = False
        self.uri = 'tcp://%s:%s' % (ip, port)

    def run(self):
        logger.info('Starting reply on: %s' % self.uri)
        self.running = True
        self.context = zmq.Context()
        self.response = self.context.socket(zmq.REP)

        try:
            self.response.bind(self.uri)
        except:
            logger.critical('Reply bind error: {0}'.format(sys.exc_info()[1]))
            self.stop()

        while self.running:
            logger.debug('Reply waiting request...')
            request = self.response.recv_json()
            logger.debug('Reply received request. %s' % request)

            try:
                getattr(self, request['action'])(request)
            except AttributeError, error:
                logger.warning('Reply received a bad request.')
                self.sendReply({'action': 'ERROR'})

            self.sendReply({'action': 'OK'})

    def registerStudent(self, request):
        studentName = request['studentName']
        protocolSignal.registerStudent.emit(studentName)

    def callAttention(self, request):
        studentName = request['studentName']
        protocolSignal.callAttention.emit(studentName)

    def sendReply(self, reply):
        logger.debug('Reply sending resonse.')
        self.response.send_json(reply)

    def stop(self):
        logger.info('Stopping reply')
        self.running = False
        self.response.close()
        self.context.term()
        self.wait()
        self.exit()
