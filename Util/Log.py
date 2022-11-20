import logging


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('Main logger')
logger.setLevel(logging.DEBUG)

# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)

def user__set_level(value):
    logger.setLevel(value)
    # ch.setLevel(value)

