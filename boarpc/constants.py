#encoding:utf-8

from common.config.conf import config
class Constants:
    SERVICE_KEY=''
    APP_MODULE_NAME = config.getConf('app','app_name','')
    APP_REGISTER_ROOT_PATH = '/boa_rpc/%s' % (APP_MODULE_NAME)
    APP_REGISTER_PROVIDER_PATH = '/boa_rpc/%s/%s' % (APP_MODULE_NAME,'providers')
    APP_REGISTER_CONSUMER_PATH = '/boa_rpc/%s/%s' % (APP_MODULE_NAME, 'consumers')
    APP_REGISTER_PROVIDER_CHILD_PATH= APP_REGISTER_PROVIDER_PATH + '/{0}'
