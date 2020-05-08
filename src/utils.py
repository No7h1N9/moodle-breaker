import logging


def to_float(s):
    try:
        return float(s)
    except ValueError:
        return -1


def setup_logger(loglevel):
    logger = logging.getLogger("main")
    logger.setLevel(loglevel)
    # create the logging file handler
    fh = logging.FileHandler("../main.log")

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger


logger = setup_logger(logging.DEBUG)