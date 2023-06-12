import logging
from logging.handlers import TimedRotatingFileHandler
import os

CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)-10s %(filename)s %(message)s')

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'logs', 'client', 'client.log')

LOG = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='M')
LOG.setFormatter(CLIENT_FORMATTER)

LOGGER = logging.getLogger('client')
LOGGER.addHandler(LOG)
LOGGER.setLevel(logging.DEBUG)