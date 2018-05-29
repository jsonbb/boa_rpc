#encoding:utf-8

class NoFoundException(Exception):
    def __str__(self):
        return 'Not find the service'

class  FatalError(Exception):
    def __str__(self):
        return 'Fatal Error'

class UnrealizedException(Exception):
    def __str__(self):
        return 'Unrealized method:' + self.message