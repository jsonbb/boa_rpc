#encoding:utf-8

import socket

class NetUtils:

    @staticmethod
    def getIp():
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def getFreePort():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port