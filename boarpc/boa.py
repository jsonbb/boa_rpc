#encoding:utf-8

import os
import sys
import glob



from boarpc.baseEndpoint import Endpoint
from boarpc.registry.registryService import RegistryFactory
from common.config.conf import config
reload(sys)
sys.setdefaultencoding('utf-8')

class BoaRpc:

    # defualt protocol: thrift
    PROTOCOL = config.getConf('rpc','protocol',defult='thrift')
    def __init__(self,coroutines=1000,url=None):
        self.endpoint_path = os.path.join(os.path.dirname(os.path.realpath(__file__)).replace('boarpc',''),'endpoint')
        sys.path.insert(0, self.endpoint_path)
        self.coroutines = coroutines
        self.url = url
    def run(self):
        from boarpc.protocol.protocol import ProtocolFactory
        protocol = ProtocolFactory.createProtocol(self.PROTOCOL,self.url)
        protocol.run()

import time
import multiprocessing
from  multiprocessing import Process

from boarpc.url import URL
from common.utils.netUtils import NetUtils
from common.util_Log.logger import logging
logger = logging.getLogger(__name__)
class MultiprocessBoa:

    PROTOCOL = config.getConf('rpc', 'protocol', defult='thrift')
    def __init__(self):
        self.endpoint_path = os.path.join(os.path.dirname(os.path.realpath(__file__)).replace('boarpc', ''), 'endpoint')
        sys.path.insert(0, self.endpoint_path)
        
    def getAllEndpoints(self):
        '''
        get all endpoints
        :return:
        '''
        for filename in glob.glob(os.path.join(self.endpoint_path, r'*.py')):
            moduleName = filename[filename.rindex(os.sep) + 1:filename.rindex('.')]
            if '__init__' != moduleName:
                __import__(moduleName)
        return Endpoint.INTERFACES
    def worker(self,url):
        a = BoaRpc(url=url)
        a.run()

    def startWorker(self):
        processes = int(config.getConf('rpc', 'processes', multiprocessing.cpu_count()))
        urlSet = set()
        portSet = set()

        # get all endpoints
        endpointSet = self.getAllEndpoints()
        host = NetUtils.getIp()
        for i in range(0, processes):
            # get a port
            port = NetUtils.getFreePort()
            if port in portSet:
                flag = True
                while flag:
                    time.time(5)
                    port = NetUtils.getFreePort()
                    if port not in portSet:
                        break
            portSet.add(port)
            url = URL(self.PROTOCOL, host, port)
            url.setEndpints(endpoints=endpointSet)
            p = Process(target=self.worker,args=(url,))
            urlSet.add(url)
            url.setProcess(p)
            p.start()
        return urlSet

    def reStartWork(self,url):
        url.setProcess(None)
        p = Process(target=self.worker, args=(url,))
        url.setProcess(p)
        p.start()


    def run(self):
        print os.getpid() 
        #start worker
        logger.info("-------start worker--------")
        urlSet = self.startWorker()
        #register to zk
        logger.info("-------register to zk--------")
        registry = RegistryFactory.createRegistry()
        registry.urlSet = urlSet
        registry.registerAll()
        for url in urlSet:
            logger.info(url)
        #monitor children process
        logger.info("-------monitor children process--------")
        while True:
            time.sleep(10)
            providers = registry.getAllProvides()
            for url in urlSet:
                p = url.process
                logger.info('Run worker process (%s) status: %s' % (p.pid,p.is_alive()))
                if not p.is_alive():
                    registry.unRegister(url)
                    p.terminate()
                    self.reStartWork(url)
                    time.sleep(5)
                    registry.register(url)
                elif url.getHostPort() not in providers:
                    #Re-register if lost in the registry
                    registry.register(url)


import  platform
from common.config.conf import config
PROTOCOL = config.getConf('rpc', 'protocol', defult='thrift')
def start():
    os_name = platform.system()
    if 'Windows' == os_name:
        MultiprocessBoa().run()
    else:
        from boarpc.protocol.tgunicorn.gunicorn_factory import GunicornFactory
        GunicornFactory.createGunicorn(PROTOCOL).run()
