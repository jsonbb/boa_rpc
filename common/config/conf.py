#-*- coding: UTF-8 -*-
from ConfigParser import ConfigParser
import os

class ConfigUtils(object):
     def __init__(self,fileName):
         super(ConfigUtils, self).__init__()
         try:
             self.path =  os.path.dirname(os.path.realpath(__file__)).replace('common','')
             self.config = ConfigParser()
             self.config.read(self.path  +"/application.cfg")
             active = self.config.get("profiles","active")
             cfgFiles = [self.path  +"/application.cfg",
                         self.path  +"/application_"+active+".cfg"]
             self.config.read(cfgFiles)
         except IOError,e:
             print  e
     def getConf(self,section, option):
         value = self.config.get(section, option)
         if(value is None or value.strip() == ''):
             return None
         return value
     def getLogConfig(self):
         return  self.path  +"/log.json"


config = ConfigUtils("")

