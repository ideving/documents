import logging
import os
from logging import handlers


def get_log(filename, level=logging.DEBUG):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    mylog = logging.getLogger()
    mylog.setLevel(level)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    # hdl = logging.FileHandler(filename=filename, mode='a', encoding='utf8')
    hdl = handlers.TimedRotatingFileHandler(filename=filename, when='D', backupCount=7, encoding='utf8')
    hdl.setFormatter(fmt)
    mylog.addHandler(hdl)
    return mylog


if __name__ == '__main__':
    log = get_log("logs/out.log")
    log.info("hello world!")
