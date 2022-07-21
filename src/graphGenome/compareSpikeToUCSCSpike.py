
import configparser

from utilities.Read import getContentOfFile

CONFIG_FILE = r'config/config.cfg'


def get_configs():
    app_config = configparser.RawConfigParser()
    app_config.read(CONFIG_FILE)
    return app_config


config = get_configs()


def compareToUCSCSpike():
    UCSCSpike = config['inputAddresses'].get('UCSCSpike')
    print(getContentOfFile(UCSCSpike))
