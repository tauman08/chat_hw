import time
from common.var import LOGGING_ON
# import logging
import traceback
import sys
# import log.conf_srv_log
# import log.conf_client_log


def log(logger):
    def decorator(func):
        if LOGGING_ON:
            def wrapper(*args, **kwargs):
                module_name = func.__module__
                # logger = logging.getLogger(module_name)
                r = func(*args, **kwargs)
                logger.info(f'Была вызвана функция {func.__name__} с параметрами {args} {kwargs}'
                            f'Вызов из модуля {module_name}'
                            f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}')
                return r
            return wrapper
        else:
            return func
    return decorator



