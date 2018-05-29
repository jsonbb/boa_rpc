#encoding:utf-8

from  boarpc.exception.exceptions import UnrealizedException

class Registry:
    PROVIDER_MD5=''
    def registerAll(self,):
        raise UnrealizedException("registerAll")

    def register(self,url):
        raise UnrealizedException("register")

    def unRegister(self, url):
        raise UnrealizedException("unRegister")

    def getProvideMD5(self):
        raise UnrealizedException("getProvideMD5")



from boarpc.registry.zookeeper.zookeeperRegistry import ZookeeperRegistry
class RegistryFactory:

    @staticmethod
    def createRegistry(registry='zookeeper'):
        return ZookeeperRegistry()
