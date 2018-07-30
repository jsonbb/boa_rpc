# -*- coding: utf-8 -*-
import time
import json
from multiprocessing import Process
import telnetlib
from kazoo.client import KazooClient
from kazoo.retry import KazooRetry
from common.util_Log.logger import logging
from boarpc.registry.registryService import RegistryFactory
from common.config.conf import config
from boarpc.url import URL

logger = logging.getLogger(__name__)




class ZkRigster(object):
    PROTOCOL = config.getConf('rpc', 'protocol', defult='thrift')

    def __init__(self,bind):
        host,port = bind.split(":")
        self.url = URL(self.PROTOCOL, host, port)

    def run(self):
        # register to zk
        logger.info("-------register to zk--------")
        registry = RegistryFactory.createRegistry()
        urlSet = set()
        urlSet.add(self.url)
        registry.urlSet = urlSet
        registry.registerAll()
        logger.info(self.url)
        # monitor children process
        while True:
            time.sleep(10)
            providers = registry.getAllProvides()
            if self.url.getHostPort() not in providers:
                    # Re-register if lost in the registry
                    registry.register(self.url)

    def register_instances(self):
        p = Process(target=self.run, args=())
        p.daemon = True
        p.start()