#-*- coding: UTF-8 -*-  

import os
import logging
import logging.config

filename_directory = "./logs/pid_%s/" % os.getpid()
if not os.path.exists(filename_directory):
    os.makedirs(filename_directory)
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] - %(name)s - %(filename)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple"
        },
        "debug_file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": "./logs/pid_%s/debug.log" % os.getpid(),
            "when":"D",
            "interval":1,
            "backupCount": 20,
            "encoding": "utf8"
        },
        "info_file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "./logs/pid_%s/info.log" % os.getpid(),
            "when":"D",
            "interval":1,
            "backupCount": 20,
            "encoding": "utf8"
        },

        "error_file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": "./logs/pid_%s/errors.log" % os.getpid(),
            "when":"D",
            "interval":1,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },



    "root": {
        "level": "INFO",
        "handlers": ["console","debug_file_handler","info_file_handler", "error_file_handler"]
    }
})


if __name__ == '__main__':
    pass