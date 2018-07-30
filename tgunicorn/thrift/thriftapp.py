# -*- coding: utf-8 -

import os
import sys

from gunicorn.app.base import Application
import gunicorn.workers
from gunicorn.six import iteritems
# `config` is unused in this module but must be imported to register config
# options with tgunicorn
from . import config
from . import utils
from .six import AVAILABLE_WORKERS

# register thrift workers

gunicorn.workers.SUPPORTED_WORKERS.update(AVAILABLE_WORKERS)


class ThriftApplication(Application):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.thrift_app = app
        self.endpoint_path = os.path.join(os.path.dirname(os.path.realpath(__file__)).replace('boarpc', ''), 'endpoint')
        sys.path.insert(0, self.endpoint_path)
        super(ThriftApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

        if self.options['worker_class'] and \
                self.options['worker_class'] not in AVAILABLE_WORKERS:
            raise ValueError

        #self.cfg.set("default_proc_name", self.options['handler'])
        #self.app_uri = self.options['handler']

    def init(self, parser, opts, args):
        print self.usage
        print self.prog
        if len(args) != 1:
            parser.error("No application name specified.")
        self.cfg.set("default_proc_name", args[0])

        self.app_uri = args[0]
        print args[0]

        if opts.worker_class and \
                opts.worker_class not in AVAILABLE_WORKERS:
            raise ValueError

    def load_thrift_app(self):
        return utils.load_obj(self.app_uri)

    def load(self):
        self.chdir()
        self.tfactory = utils.load_obj(self.cfg.thrift_transport_factory)()
        self.pfactory = utils.load_obj(self.cfg.thrift_protocol_factory)()
        #self.thrift_app = self.load_thrift_app()
        return lambda: 1

    def chdir(self):
        os.chdir(self.cfg.chdir)
        sys.path.insert(0, self.cfg.chdir)

    def run(self):
        if self.cfg.service_register_cls:
            service_register_cls = utils.load_obj(
                self.cfg.service_register_cls)
            self.service_watcher = service_register_cls(
                self.cfg.bind[0])
            self.service_watcher.register_instances()
        super(ThriftApplication, self).run()
