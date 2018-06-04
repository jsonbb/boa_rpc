#encoding:utf-8

import os
import sys
import glob


from boarpc.protocol.protocol import ProtocolFactory
from boarpc.baseEndpoint import Endpoint
from common.config.conf import config
reload(sys)
sys.setdefaultencoding('utf-8')

class BoaRpc:

    # defualt protocol: thrift
    PROTOCOL = config.getConf('rpc','protocol',defult='thrift')
    def __init__(self,coroutines=1000):
        self.endpoint_path = os.path.join(os.path.dirname(os.path.realpath(__file__)).replace('boarpc',''),'endpoint')
        sys.path.insert(0, self.endpoint_path)
        self.coroutines = coroutines

    def getAllEndpoints(self):
        for filename in glob.glob(os.path.join(self.endpoint_path,r'*.py')):
            moduleName = filename[filename.rindex(os.sep)+1:filename.rindex('.')]
            if '__init__' != moduleName:
                __import__(moduleName)
        return Endpoint.INTERFACES


    def run(self):
        protocol = ProtocolFactory.createProtocol(self.PROTOCOL)
        # get all endpoints
        protocol.getURL().setEndpints(self.getAllEndpoints())
        protocol.run()



# print  os.path.join(os.path.dirname(os.path.realpath(__file__)).replace('boarpc',''),'endpoint')
