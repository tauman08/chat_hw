import logging
from logging.handlers import TimedRotatingFileHandler
import os

SRV_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'logs', 'server', 'server.log')

LOG = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='M')
LOG.setFormatter(SRV_FORMATTER)

LOGGER = logging.getLogger('server')
LOGGER.addHandler(LOG)
LOGGER.setLevel(logging.DEBUG)