import logging
import sys


def to_float(s: str):
    if s is None:
        return s
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return -1


def to_int(s: str):
    if s is None:
        return None
    try:
        return int(s)
    except ValueError:
        return -1


def setup_logger(loglevel):
    logger = logging.getLogger("")
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(loglevel)
    # create the logging file handler
    fh = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(funcName)s - %(message)s"
    )
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger


logger = setup_logger(logging.INFO)
