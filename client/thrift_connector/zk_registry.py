#encoding:utf-8

import sys
import signal


from kazoo.client import KazooClient
from kazoo.retry import KazooRetry
from kazoo.client import KazooState
from kazoo.exceptions import NodeExistsError

from common.config.conf import config
from common.util_Log.logger import logging
from common.utils.netUtils import NetUtils
logger = logging.getLogger(__name__)
from .client_pool import MultiClientPool
from boarpc.protocol.thrift import BoarpcService

APP_REGISTER_PROVIDER_PATH = '/boa_rpc/%s/providers'
APP_REGISTER_CONSUMER_PATH = '/boa_rpc/%s/consumers'

class ZookeeperRegistry(object):

    APP_DICT = dict()


    def __init__(self):
        connectionRetry = KazooRetry(max_tries=-1)
        timeout = 60
        self.zkClient = KazooClient(hosts=config.getConf('rpc', 'zk_host'), timeout=timeout, connection_retry=connectionRetry)
        self.zkClient.start(timeout=60)

        signal.signal(signal.SIGINT, self.close)
        @self.zkClient.add_listener
        def stateListener(state):
            if state == KazooState.CONNECTED:
                if ZookeeperRegistry.isRegister:
                    logger.info('ZooKeeper listener reconnected')
                    self.zkClient.handler.spawn(self.recover)
                ZookeeperRegistry.isRegister = True


    def __addAppListener(self,appName):
        __APP_REGISTER_PROVIDER_PATH = APP_REGISTER_PROVIDER_PATH % (appName)
        __APP_REGISTER_CONSUMER_PATH = APP_REGISTER_CONSUMER_PATH % (appName)

        if self.createPersistent(__APP_REGISTER_PROVIDER_PATH):
            @self.zkClient.ChildrenWatch(__APP_REGISTER_PROVIDER_PATH)
            def watch_children(childrens):
                logger.info(u'更新服务列表: %s' % childrens)
                if not childrens or len(childrens)==0:
                    self.__delApp(appName)
                else:
                    old_servers = self.APP_DICT[appName].get_servers() or []
                    servers = list()
                    for child in childrens:
                        protocol,host,port = child.split(':')
                        servers.append((host,int(port)))
                    for oserver in old_servers:
                        if oserver not in servers and self.APP_DICT[appName].produce_client(oserver[0],oserver[1]).test_connect():
                            servers.append(oserver)
                    self.APP_DICT[appName].set_servers(servers)

        if self.createPersistent(__APP_REGISTER_CONSUMER_PATH):
            self.createEphemeral(__APP_REGISTER_CONSUMER_PATH+"/"+NetUtils.getIp())


    def addApp(self,appName):
        if not self.APP_DICT.has_key(appName):
            self.APP_DICT.setdefault(appName,MultiClientPool(service=BoarpcService, servers=[], keepalive=60))
            self.__addAppListener(appName)
        return self.APP_DICT.get(appName)

    def __delApp(self,appName):
        if self.APP_DICT.has_key(appName):
            client = self.APP_DICT.pop(appName)
            client.clear()
            client = None

    def recover(self):
        for appName in self.APP_DICT.keys():
            self.__addAppListener(appName)

    def close(self):
        self.zkClient.close()

    def getClient(self,appName):
        return self.APP_DICT.get(appName) if self.APP_DICT.has_key(appName) else None

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


