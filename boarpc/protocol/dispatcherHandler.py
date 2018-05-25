#encoding:utf-8

import time
import importlib

import demjson as json

from boarpc.exception.exceptions import NoFoundException
from common.util_Log.logger import logging
logger = logging.getLogger(__name__)

class DispatcherHandler:

    def dispatcher(self, client, moduleName, className, functionName, params):
        """
        Parameters:
         - client
         - moduleName
         - className
         - functionName
         - params
        """
        start_time = time.time()
        decode_leaves = map(lambda x: x.decode('utf-8'), params)
        interface_path = '.'.join([moduleName, className, functionName])
        logger.info(u'客户端请求：%s，接口调用：%s' % (client, interface_path))
        # reload(__import__(root))
        cls = getattr(importlib.import_module(moduleName), className)
        if interface_path not in cls.INTERFACES:
            raise NoFoundException()
        obj = cls()
        try:
            result = getattr(obj, functionName)(*decode_leaves)
            value = result if isinstance(result, basestring) else json.encode(result,encoding='utf-8')
            logger.info("%s take time : %f" % (functionName, time.time() - start_time))
            return value.encode('utf-8') if isinstance(value, unicode) else value
        except Exception as  ex:
            logger.exception(ex)
            # raise ex
