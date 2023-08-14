import logging
import nexfil.share


def log_writer(message):
    logging.basicConfig(
        filename=nexfil.share.LOG_FILE_PATH,
        encoding='utf-8',
        level=logging.INFO,
        format='[%(asctime)s] : %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logging.info(message)
