#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

# reload(sys)
# sys.setdefaultencoding("utf-8")

class DateUtils:
    @staticmethod
    def formatNow(pattern = '%Y-%m-%d %H:%M:%S'):
        return time.strftime(pattern,time.localtime(time.time()))