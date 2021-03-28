#logger settings
import logging
import sys
import colorlog

logger = logging.getLogger('')
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(colorlog.ColoredFormatter('%(log_color)s [%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S'))
logger.addHandler(sh)


def hello_logger():
    logger.info("Hello info")
    logger.critical("Hello critical")
    logger.warning("Hello warning")
    logger.debug("Hello debug")
    logger.error("Error message")


if __name__=="__main__":
    hello_logger()

