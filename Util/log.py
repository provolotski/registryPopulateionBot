import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('Main logger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def user_set_level(value):
    logger.setLevel(value)
