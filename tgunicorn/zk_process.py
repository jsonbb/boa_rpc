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
        registry.PROVIDER_MD5 = registry.getProvideMD5()
        # monitor children process
        while True:
            time.sleep(10)
            md5 = registry.getProvideMD5()
            if registry.PROVIDER_MD5 != md5:
                registry.PROVIDER_MD5 = md5
                registry.register(self.url)
            # for url in urlSet:
            #     p = url.process
            #     logger.info('Run worker process (%s) status: %s' % (p.pid, p.is_alive()))
            #     if not p.is_alive():
            #         registry.unRegister(url)
            #         p.terminate()
            #         self.reStartWork(url)
            #         time.sleep(5)
            #         registry.register(url)
            #     elif flag:
            #         registry.register(url)

    def register_instances(self):
        p = Process(target=self.run, args=())
        p.daemon = True
        p.start()




class ZkProcess(Process):

    def __init__(self,zk_cfg,):
        super(ZkProcess, self).__init__()
        self.zk_cfg = zk_cfg
        logger.info("zk register info [%s] !" % (str(zk_cfg)))

    def run(self):
        # zk client
        connection_retry = KazooRetry(max_tries=(self.zk_cfg["zk_tries"] if self.zk_cfg["zk_tries"] else -1))
        timeout = self.zk_cfg["zk_timeout"] if self.zk_cfg["zk_timeout"] else 60
        heart_time = self.zk_cfg["heart_time"] if self.zk_cfg["heart_time"] else 60
        self.zk_client = KazooClient(hosts=self.zk_cfg["addr"], timeout=timeout, connection_retry=connection_retry)
        self.zk_client.start(timeout=timeout)
        register_tries = self.zk_cfg["register_tries"] if self.zk_cfg["register_tries"] else 10
        while register_tries>0:
            host,port = self.zk_cfg['bind'].split(":")
            try:
                telnetlib.Telnet(host, port)
                self.register(self.zk_cfg['path'],self.zk_cfg['bind'])
            except Exception as e:
                logger.error("service [%s] losted"%(self.zk_cfg['bind']))
                register_tries = register_tries-1

            time.sleep(heart_time)

    # 向ZooKeeper注册信息
    def register(self, register_path, key, value=None):
        self.zk_client.ensure_path(register_path)
        logger.info("zk service node %s !" % (str(self.zk_client.get_children(register_path))))
        node = '/'.join([register_path, key])
        if self.zk_client.exists(node):
            return
        path = self.zk_client.create(node, ephemeral=True)
        logger.info("zk registered [%s] !"%(key))
        if value and isinstance(value, dict):
            value['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(time.time())))
            value['timestamp'] = int(time.time())
            dumps_value = json.dumps(value, ensure_ascii=False).encode('utf-8')
            self.zk_client.set(path, dumps_value)


