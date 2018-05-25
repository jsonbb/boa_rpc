#encoding:utf-8

from common.config.conf import config
from boarpc.exception.exceptions import UnrealizedException

class IProtocol:

    def getRegisterPath(self):
        return '/doa_rpc/%s' % config.getConf('app','app_name','')
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
    def createProtocol(protocol):
         if 'thrift'== protocol:
             return ThriftProtocol()
         else:
             raise FatalError('Nonsupport protocol')


