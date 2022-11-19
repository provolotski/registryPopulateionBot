import json
import XmlLoader
import Util.config as conf



def test_get_work():
    test = '{"@ID": "28183765", "ID": "28183765", "SID": "125477146", "FSZN_UNN": "100036095", "FSZN_BEGIN_DATE": "01.01.2003", "FSZN_END_DATE": "06.03.2014"}'
    test2 ='[{"@ID": "28183765", "ID": "28183765", "SID": "125477146", "FSZN_UNN": "100036095", "FSZN_BEGIN_DATE": "01.01.2003", "FSZN_END_DATE": "06.03.2014"},{"@ID": "28183765", "ID": "28183765", "SID": "125477146", "FSZN_UNN": "100036095", "FSZN_BEGIN_DATE": "01.01.2003", "FSZN_END_DATE": "06.03.2014"}]'
    json_object = json.loads(test2)

    print(XmlLoader.get_work(json_object))
    assert True

def test_config():
    print (conf.oracle_user)
    assert True