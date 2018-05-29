#encoding:utf-8

from thrift.server.TServer import TServer
from thrift.transport.TTransport import TTransportException
from gevent.pool import Pool
import gevent.monkey
gevent.monkey.patch_all()

from common.util_Log.logger import logging
logger = logging.getLogger(__name__)

class TGeventPoolServer(TServer):
    """Server with a fixed size pool of coroutines which service requests."""
    def __init__(self, *args):
        TServer.__init__(self, *args)
        self.coroutines = 500

    def setNumCoroutines(self, num):
        """Set the number of worker coroutines that should be created"""
        self.coroutines = num


    def serveClient(self, client):
        """Process input/output from a client for as long as possible"""
        itrans = self.inputTransportFactory.getTransport(client)
        otrans = self.outputTransportFactory.getTransport(client)
        iprot = self.inputProtocolFactory.getProtocol(itrans)
        oprot = self.outputProtocolFactory.getProtocol(otrans)
        try:
            while True:
                self.processor.process(iprot, oprot)
        except TTransportException:
            pass
        except Exception as x:
            logger.exception(x)

        itrans.close()
        otrans.close()

    def serve(self):
        # Pump the socket for clients
        self.serverTransport.listen()
        pool = Pool(int(self.coroutines))
        while True:
            try:
                client = self.serverTransport.accept()
                if not client:
                    continue
                pool.spawn(self.serveClient, client)
            except Exception as x:
                logger.exception(x)