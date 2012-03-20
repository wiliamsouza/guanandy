"""
Utilities used across all modules.

"""

import os
import sys
import csv
import fcntl
import struct
import socket
import logging

logger = logging.getLogger(__name__)


EMPTY_VALUES = (None, '', [], (), {})

def isPlatformLinux():
    """
    Return True is platform is linux False otherwise
    """
    return sys.platform.startswith('linux')

def isPlatformWindows():
    """
    Return True is platform is windows False otherwise
    """
    return sys.platform.startswith('win')

def homeDirectory():
    """
    Return the current user home directory
    """
    if isPlatformLinux():
        return os.getenv('HOME')
    else:
        return os.getenv('USERPROFILE')

def ipAddress():
    """
    Return a non local ip address
    """
    logger.debug('Trying to get ip address from socket.')
    try:
        ip = socket.gethostbyname(socket.gethostname())
        if not ip.startswith('127'):
            logger.debug('Ip {0} address found.'.format(ip))
            return ip
    except socket.gaierror:
        logger.debug('Getting ip address from socket failed.')

    logger.debug('Trying to get ip address using netifaces.')
    try:
        import netifaces
        for interface in netifaces.interfaces():
            try:
                ip = netifaces.ifaddresses(interface) \
                        [netifaces.AF_INET][0]['addr']
                if not ip.startswith('127'):
                    logger.info('Ip {0} address found on {1}'.format(ip,
                        interface))
                    return ip
            except KeyError:
                pass
        logger.debug('Getting ip address from netifaces failed.')
    except ImportError:
        logger.debug('netifaces not installed.')

    if isPlatformLinux():
        logger.debug('Trying to get ip address from /proc/net/route')
        routeFile  = open('/proc/net/route', 'r')
        for route in csv.DictReader(routeFile, delimiter='\t'):
            if long(route['Destination'], 16) == 0:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    ip = socket.inet_ntoa(fcntl.ioctl(sock.fileno(),
                        0x8915, struct.pack('256s',
                            route['Iface'][:15]))[20:24])
                    if not ip.startswith('127'):
                        logger.debug('Ip {0} address found.'.format(ip))
                        return ip
                except IOError:
                    pass
        logger.debug('Getting ip address from /proc/net/route failed.')

    if isPlatformWindows():
        logger.debug('Trying to get ip from WMI')
        try:
            import wmi
            for interface in wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=1):
                   return interface.IPAddress
        except ImportError:
            logger.debug('wmi not installed.')
        logger.debug('Getting ip address from wmi failed.')

    # TODO: Raise an execption here not return None
    return None
