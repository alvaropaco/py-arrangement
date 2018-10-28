import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class Logger:
     def __init__(self, app):
        logFileName = "log/{now}:debug.log".format(now=datetime.now())
        print('Starting application...')
        print('Loggin into {fileName}'.format(fileName=logFileName))
        formatter = logging.Formatter(
            "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        handler = RotatingFileHandler(
            logFileName, maxBytes=10000000, backupCount=5)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.DEBUG)
        log.addHandler(handler)