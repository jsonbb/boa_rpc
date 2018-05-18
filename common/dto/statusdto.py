#!/usr/bin/python
# -*- coding: utf-8 -*-

class Status:
    @staticmethod
    def ok(data,msg='ok'):
        return {'code':"200",'data':data,'msg':msg}

    @staticmethod
    def error(data,msg='ok'):
        return {'code':"500",'data':data,'msg':msg}