import logging

logger = logging.getLogger(__name__)


def log(msg: str):
    logging.basicConfig(level=logging.INFO)
    logger.info("Started ---------------->")
    logger.info(msg)
    logger.info("<--------------- Finished")
