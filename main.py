#encoding:utf-8
__author__ = 'js'
from boarpc.boa import BoaRpc
from common.util_Log.logger import logging
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    a = BoaRpc()
    a.run()