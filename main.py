#encoding:utf-8


from boarpc.boa import MultiprocessBoa
from common.util_Log.logger import logging
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    a = MultiprocessBoa()
    a.run()
