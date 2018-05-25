#encoding:utf-8

from boarpc.exception.exceptions import FatalError
from common.util_Log.logger import logging
logger = logging.getLogger(__name__)
import inspect
class Endpoint:
    INTERFACES = set()
    @staticmethod
    def register(interface):
        endpointUrl =  interface.__module__+'.'+inspect.stack()[1][3]+'.'+interface.__name__
        if endpointUrl not in Endpoint.INTERFACES:
            logger.info("register endpoint: [ %s ] " % endpointUrl)
            Endpoint.INTERFACES.add(endpointUrl)
        else:
            logger.error('Duplicate endpoint [{0}]'.format(str(interface)))
            raise FatalError()
        return interface
