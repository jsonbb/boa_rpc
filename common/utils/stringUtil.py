#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
class StringUtils:
    @staticmethod
    def coverType(type, value):
        if value == '' or value is None:
            return 0
        if 'int' == type or 'bool' == type:
            return int(float(value))
        elif 'double' == type or 'float' == type:
            return float(value)
        elif 'array' == type:
            return str(value).split(',')
        elif 'json' == type:
            return json.loads(value)
        else:
            return value