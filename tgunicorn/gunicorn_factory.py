# -*- coding: utf-8 -

class GunicornProtocol(object):
    @staticmethod
    def on_exit(server):
        from common.config.conf import config
        from boarpc.url import URL
        from boarpc.registry.registryService import RegistryFactory
        host, port = server.app.cfg.bind[0].split(":")
        registry = RegistryFactory.createRegistry()
        registry.unRegister(URL(config.getConf('rpc', 'protocol', defult='thrift'), host, port))


    def thrift(self):
        from tgunicorn.thrift.thriftapp import ThriftApplication
        from boarpc.protocol.thrift import BoarpcService
        from boarpc.protocol.dispatcherHandler import DispatcherHandler
        from common.utils.netUtils import NetUtils
        from common.config.conf import config
        import multiprocessing


        handler = DispatcherHandler()
        app = BoarpcService.Processor(handler)

        bind = "%s:%s" % (NetUtils.getIp(), str(NetUtils.getFreePort()))
        options = {
            'worker_class' : 'thrift_gevent',
            'thrift_protocol_factory' : 'thrift.protocol.TCompactProtocol:TCompactProtocolAcceleratedFactory',
            'thrift_transport_factory' : 'thrift.transport.TTransport:TBufferedTransportFactory',
            'service_register_cls' : 'tgunicorn.zk_process:ZkRigster',
            'bind': bind,
            'workers': int(config.getConf('rpc', 'processes', multiprocessing.cpu_count())),
            'on_exit' : GunicornProtocol.on_exit,
            'daemon' : config.getConf('profiles', 'active', 'dev')=='prod',
            'reuse-port' : True ,
        }

        return ThriftApplication(app,options)


class GunicornFactory(object):
    gunicornProtocol = GunicornProtocol()

    @classmethod
    def createGunicorn(cls,protocol):
        return getattr(cls.gunicornProtocol, protocol)(*[])