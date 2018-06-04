#encoding:utf-8


from common.config.conf import config

class URL:

    def __init__(self,protocol,host,port):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.path = '/doa_rpc/%s' % config.getConf('app', 'app_name', '')
        self.process = None
        self.endpoints = set()

    def setEndpints(self,endpoints):
        self.endpoints = endpoints

    def getRegisterPath(self):
        return self.path

    def getEndpoints(self):
        return ','.join(self.endpoints)

    def setProcess(self,p):
        self.process = p

    def getHostPort(self):
        return "%s:%s:%s" % (self.protocol,self.host,self.port)


    def __str__(self):
        return "{0}:{1}:{2}:{3}:{4}".format(self.protocol,self.host,self.port,self.path,','.join(self.endpoints))

if __name__ == '__main__':
    pass