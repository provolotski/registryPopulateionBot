import json

import pytest

testXML ='{"UN_PERSON":{"SID": "180649375", "UN_FSZN": [{"FSZN_UNN": "191519009", "FSZN_BEGIN_DATE": "16.06.2012", "FSZN_END_DATE": "03.10.2014"}, {"FSZN_UNN": "190174249",  "FSZN_BEGIN_DATE": "01.01.2003", "FSZN_END_DATE": "21.05.2003"}, { "FSZN_UNN": "300550100", "FSZN_BEGIN_DATE": "15.09.2008", "FSZN_END_DATE": "15.06.2010"}, { "FSZN_UNN": "190546077", "FSZN_BEGIN_DATE": "14.04.2005", "FSZN_END_DATE": "12.09.2008"} , {"FSZN_UNN": "690776338", "FSZN_BEGIN_DATE": "01.12.2010", "FSZN_END_DATE": "10.10.2011"}, {"FSZN_UNN": "100598494", "FSZN_BEGIN_DATE": "18.10.2003", "FSZN_END_DATE": "13.04.2005"}, {"FSZN_UNN": "191397650", "FSZN_BEGIN_DATE": "11.10.2011", "FSZN_END_DATE": "15.06.2012"}, {"FSZN_UNN": "190000166", "FSZN_BEGIN_DATE": "12.11.2014", "FSZN_END_DATE": "30.06.2016"},{"FSZN_UNN": "600112292", "FSZN_BEGIN_DATE": "06.07.2016", "FSZN_END_DATE": "None"}]}}'
#
import OracleUtils


def test_connect_db():
    assert OracleUtils.connect_db() == 'X'


def test_get_work():
    assert OracleUtils.get_work(191519009) =='ООО "ДАВКОЛДЕН"'
    json_object = json.loads(testXML)
    print(json_object)
