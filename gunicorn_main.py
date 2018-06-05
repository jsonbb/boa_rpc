#encoding:utf-8
__author__ = 'js'
from common.util_Log.logger import logging
logger = logging.getLogger(__name__)

from tgunicorn.gunicorn_factory import GunicornFactory

from common.config.conf import config
PROTOCOL = config.getConf('rpc', 'protocol', defult='thrift')

if __name__ == '__main__':

    GunicornFactory.createGunicorn(PROTOCOL).run()
