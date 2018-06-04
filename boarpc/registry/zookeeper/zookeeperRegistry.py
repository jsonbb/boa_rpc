#encoding:utf-8

import sys
import signal


from kazoo.client import KazooClient
from kazoo.retry import KazooRetry
from kazoo.client import KazooState
from kazoo.exceptions import NodeExistsError

from boarpc.registry.registryService import Registry
from boarpc.constants import Constants
from common.utils.md5Utils import Md5Utils
from common.config.conf import config
from common.util_Log.logger import logging
logger = logging.getLogger(__name__)

class ZookeeperRegistry(Registry):
    isRegister=False
    def __init__(self):
        connectionRetry = KazooRetry(max_tries=-1)
        timeout = 60
        self.zkClient = KazooClient(hosts='127.0.0.1:2181', timeout=timeout, connection_retry=connectionRetry)
        self.zkClient.start(timeout=60)
        self.urlSet = set()
        signal.signal(signal.SIGINT, self.close)
        @self.zkClient.add_listener
        def stateListener(state):
            if state == KazooState.CONNECTED:
                if ZookeeperRegistry.isRegister:
                    logger.info('ZooKeeper listener reconnected')
                    self.zkClient.handler.spawn(self.registerAll)
                ZookeeperRegistry.isRegister = True



    def registerAll(self):
        urls = set(self.urlSet)
        url = urls.pop()
        if self.createPersistent(Constants.APP_REGISTER_ROOT_PATH,url.getEndpoints()) and self.createPersistent(Constants.APP_REGISTER_PROVIDER_PATH) and self.createPersistent(Constants.APP_REGISTER_CONSUMER_PATH):
            self.createEphemeral(Constants.APP_REGISTER_PROVIDER_CHILD_PATH.format(url.getHostPort()))
            for u in urls:
                self.createEphemeral(Constants.APP_REGISTER_PROVIDER_CHILD_PATH.format(u.getHostPort()))

    def register(self,url):
        if self.createPersistent(Constants.APP_REGISTER_ROOT_PATH, url.getEndpoints()) and self.createPersistent(
                Constants.APP_REGISTER_PROVIDER_PATH) and self.createPersistent(Constants.APP_REGISTER_CONSUMER_PATH):
            self.createEphemeral(Constants.APP_REGISTER_PROVIDER_CHILD_PATH.format(url.getHostPort()))


    def unRegister(self, url):
        providerPath = Constants.APP_REGISTER_PROVIDER_CHILD_PATH.format(url.getHostPort())
        if self.zkClient.exists(providerPath):
            self.zkClient.delete(providerPath)

    def getProvideMD5(self):
        providers = self.zkClient.get_children(Constants.APP_REGISTER_PROVIDER_PATH)
        if providers is not None  :
            providers.sort()
            return Md5Utils.md5(''.join(providers))




    def close(self,signum, frame):
        self.zkClient.close()

    def createPersistent(self,path,value=b''):
        try:
            self.zkClient.ensure_path(path)
            self.zkClient.set(path,value=value)
        except NodeExistsError as ne:
            logger.exception(ne)


        return True

    def createEphemeral(self,path,value=b''):
        try:
            if self.zkClient.exists(path) is None:
                self.zkClient.create(path, value=value,ephemeral=True)
        except NodeExistsError as ne:
            logger.exception(ne)
        return True


