#encoding:utf-8

from common.config.conf import config
class Constants:
    SERVICE_KEY=''
    PROJECT_NAME = config.getConf('app', 'project_name', '')
    APP_MODULE_NAME = config.getConf('app','app_name','')
    APP_REGISTER_ROOT_PATH = '/%s_boa_rpc/%s' % (PROJECT_NAME,APP_MODULE_NAME)
    APP_REGISTER_PROVIDER_PATH = '/%s_boa_rpc/%s/%s' % (PROJECT_NAME,APP_MODULE_NAME,'providers')
    APP_REGISTER_CONSUMER_PATH = '/%s_boa_rpc/%s/%s' % (PROJECT_NAME,APP_MODULE_NAME, 'consumers')
    APP_REGISTER_PROVIDER_CHILD_PATH= APP_REGISTER_PROVIDER_PATH + '/{0}'
