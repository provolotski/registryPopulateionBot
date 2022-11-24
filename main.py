import os

import Util.config
import Util.log
import XmlLoader
from Databases import MongoUtils

files = ['']

if __name__ == '__main__':
    Util.config.init_values()
    folder = os.environ['DIR']
    Util.config.set_log_level()
    for i in range(1, 14):
        XmlLoader.get_xml("{0}RN_{1}.xml".format(folder, str(i)))
    for i in range(1, 5):
        MongoUtils.check_relative(i)
