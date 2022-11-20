import os

import Util.config
import Util.Log
import XmlLoader
import Databases.OracleUtils

if __name__ == '__main__':
    Util.config.init_values()
    Util.Log.logger.debug(os.environ['FILE'])
    XmlLoader.get_xml(os.environ['FILE'])
