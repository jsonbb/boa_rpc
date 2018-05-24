#encoding:utf-8


class URL:

    def __init__(self,protocol,host,port,path):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.path = path
        self.endpoints = set()

    def setEndpints(self,endpoints):
        self.endpoints = endpoints

    def __str__(self):
        return "{0}:{1}:{2}:{3}:{4}".format(self.protocol,self.host,self.port,self.path,','.join(self.endpoints))

if __name__ == '__main__':
    pass