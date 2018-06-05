# -*- coding: utf-8 -*-

DEFAULT_WORKER = "thrift_sync"
DEFAULT_TRANSPORT = "thrift.transport.TTransport:TBufferedTransportFactory"
DEFAULT_PROTOCOL = "thrift.protocol.TBinaryProtocol:TBinaryProtocolAcceleratedFactory"
AVAILABLE_WORKERS = {
    'thrift_sync': 'tgunicorn.thrift.sync_worker.SyncThriftWorker',
    'thrift_gevent': 'tgunicorn.thrift.gevent_worker.GeventThriftWorker',
    }
