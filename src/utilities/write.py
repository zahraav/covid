import logging

logger = logging.getLogger(__name__)


def saveToFile(data, address):
    """
    This method gets a data and an address and write the data on the following
    :param data:
    :param address:
    :return:
    """
    try:
        with open(address, 'a', encoding='utf-8') as f1:
            f1.write(str(data) + "\n")

    except MemoryError as e:
        logger.error(e)
