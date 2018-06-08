#! /usr/bin/env python
# -*- coding: utf-8 -*-
from client.thrift_connector.boa_client import BoaClient

client = BoaClient()
print client.request('test_name.endpoint.demoEndpoint.Demo.test',['44'])


