namespace py boarpc.protocol.thrift

service BoarpcService {
  string dispatcher(1:string client, 2:string moduleName, 3:string className, 4:string functionName, 5:list<string> params)
}
