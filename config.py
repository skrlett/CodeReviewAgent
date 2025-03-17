import logging


def setup_logging(name):
    logging.basicConfig(filename="app.log", level=logging.INFO)
    logger = logging.getLogger(name)
    return logger
