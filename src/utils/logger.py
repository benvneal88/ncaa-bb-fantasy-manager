import logging


def get_logger(name=__name__, log_level='INFO'):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        ch = logging.StreamHandler()

        if log_level.lower() == 'info':
            logger.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
