#encoding:utf-8

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol

from boarpc.protocol.thrift import  BoarpcService
from boarpc.protocol.protocol import IProtocol
from boarpc.protocol.thrift.protocolImpl.TGeventPoolServer import TGeventPoolServer
from boarpc.url import URL
from common.utils.netUtils import NetUtils
from boarpc.protocol.dispatcherHandler import DispatcherHandler
from common.config.conf import config
from common.util_Log.logger import logging
logger = logging.getLogger(__name__)

class ThriftProtocol(IProtocol):

    def __init__(self):
        self.url = URL('thrift',NetUtils.getIp(),NetUtils.getFreePort(),self.getRegisterPath())

    def getURL(self):
        '''get url'''
        return self.url

    def run(self):
        '''
        run service
        :return:
        '''
        handler = DispatcherHandler()
        processor = BoarpcService.Processor(handler)
        transport = TSocket.TServerSocket(self.url.host, self.url.port)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TCompactProtocol.TCompactProtocolFactory()
        server = TGeventPoolServer(processor, transport, tfactory, pfactory)
        server.setNumCoroutines(config.getConf('rpc','coroutines',1000))
        logger.info(u'Set the maximum number of the coroutine：%s' % server.coroutines)
        logger.info('the URL is :[ %s ] ' % self.url)
        logger.info('starting success ')
        server.serve()

