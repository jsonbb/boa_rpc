Boa_rpc
====
Boa_rpc is based on the distributed RPC service framework developed by thrift (expandable to other protocols)

## Architecture
![](https://github.com/jsonbb/boa_rpc/blob/master/image/boa_architecture.png)

## Feature
-  the server automatically registers
-  client service automatic discovery
-  client load balancing
-  service fault tolerance

## Python dependency
-  thrift==0.11.0
-  gevent==1.3.1
-  kazoo==2.4.0
-  gunicorn==19.3.0
-  demjson==2.2.4
## example