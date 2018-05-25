#encoding:utf-8
__author__ = 'js'
from boarpc.baseEndpoint import Endpoint

class Demo(Endpoint):

    @Endpoint.register
    def test(self,param):
        print param
        print type(param)
        return {'code':1,'data':{'1':0},'msg':'ok'}

    def test2(self, param):
        print param
        return {'code': 1, 'data': {'1': 0}, 'msg': 'ok'}

class Demo2(Endpoint):

    @Endpoint.register
    def test2(self,param):
        print param
        print type(param)
        return {'code':1,'data':{'1':0},'msg':'ok'}

    def test5(self, param):
        print param
        return {'code': 1, 'data': {'1': 0}, 'msg': 'ok'}