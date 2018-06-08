# -*- coding: utf-8 -*-

import logging
from client.thrift_connector.zk_registry import ZookeeperRegistry
from common.utils.netUtils import NetUtils
logger = logging.getLogger(__name__)


class BoaClient(object):
    zkRegistry = ZookeeperRegistry()

    def request(self,endpoint,param):
        endpoints = endpoint.split('.')
        appName = endpoints[0]
        client = self.zkRegistry.addApp(appName)
        #client.maintain_connections()
        logger.info("pool size: %s" % (str(client.pool_size())))
        logger.info("request from:%s; app:%s; path:%s; class:%s; method:%s; param:%s;" % (NetUtils.getIp(),appName,'.'.join(endpoints[1:-2]),endpoints[-2],endpoints[-1],str(param)))
        return client.dispatcher(NetUtils.getIp(),'.'.join(endpoints[1:-2]),endpoints[-2],endpoints[-1],list(param))



if __name__ == '__main__':
    pass
    #client = BoaClient()
    #print client.request('test_name.endpoint.demoEndpoint.Demo.test',['44'])