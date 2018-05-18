#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib

class Md5Utils:
    @staticmethod
    def md5(content):
        hm = hashlib.md5()
        hm.update(content)
        return str(hm.hexdigest())

