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
python2.7+
-  thrift==0.11.0
-  gevent==1.3.1
-  kazoo==2.4.0
-  gunicorn==19.3.0
-  demjson==2.2.4
## example

Define service
```python
from boarpc.baseEndpoint import Endpoint

class HelloWorld(Endpoint):

    @Endpoint.register
    def test(self,param):
        print param
        return {'code':1,'data':{'1':0},'msg':'ok'}
```

Invoke service
<br>python client
```python client
from client.thrift_connector.boa_client import BoaClient

client = BoaClient()
print client.request('app_name.helloWorldEndpoint.HelloWorld.test',['44'])
```
java client
```java
 BoaConf conf = new BoaConf("10.28.102.136:2181");
 BoaClient client = new BoaClient(conf);
 Map paramMap = new HashMap<>();
 paramMap.put("id","`123456yt");
 Map re = client.request("app_name.helloWorldEndpoint.HelloWorld.test",paramMap);
```
