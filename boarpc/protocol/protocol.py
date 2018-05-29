#encoding:utf-8

from common.config.conf import config
from boarpc.exception.exceptions import UnrealizedException

class IProtocol:


    def getURL(self):
        '''get url'''
        raise UnrealizedException()

    def run(self):
        '''
        run service
        :return:
        '''
        raise UnrealizedException()


from  boarpc.protocol.thrift.protocolImpl.thriftProtocol import ThriftProtocol
from boarpc.exception.exceptions import FatalError
class ProtocolFactory:

    @staticmethod
    def createProtocol(protocol,url=None):
         if 'thrift'== protocol:
             return ThriftProtocol(url)
         else:
             raise FatalError('Nonsupport protocol')


