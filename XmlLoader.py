import xmltodict
import Util.Log as Log
from Databases import MongoUtils, OracleUtils

# {  'UN_FAMILY', 'UN_ADDRESS'
#
#
#
#
# }



def get_xml(file_name):
    """
    отработка xml и занесение его mongo
    :param file_name: название файла
    """
    try:
        from lxml import etree
    except ImportError:
        import xml.etree.cElementTree as etree
    tree = etree.parse(file_name)
    Log.logger.info('file uploaded')
    # client = MongoUtils.get_database()
    Log.logger.info('connected to Mongo')
    for person in tree.findall('UN_PERSON'):
        o = (xmltodict.parse(etree.tostring(person)))
        o1 = generate_new_structure(o['UN_PERSON'])
        # test_value = 'UN_ADDRESS'
        # if test_value in o['UN_PERSON']:
        #     Log.logger.debug(f'Информация по структуре {test_value}: {o["UN_PERSON"][test_value]} ' )
        # # id = MongoUtils.insert_document(client, o1)
        # Log.logger.info('Загружен пользователь %s ', o1['LastName'])


def generate_new_structure(document):
    """
    формируем запись по человеку
    :param document: входящий документ
    :return:
    """
    new_document = {}
    new_document['ID'] = document['ID']
    new_document['LIN'] = document['IDENTIF']
    new_document['LastName'] = init_cap(document['SURNAME'])
    new_document['FirstName'] = init_cap(document['NAME'])
    new_document['MiddleName'] = init_cap(document['SNAME'])
    new_document['BirthDate'] = document['BIRTH_DATE']
    new_document['BirthPlace'] = repl_str(document['AREA_B'], document['REGION_B'], document['LEX_TYPE_CITY_B'],
                                          document['CITY_B'])
    new_document['Sex'] = document['LEX_SEX']
    # if "UN_FSZN" in document:
    #     new_document['Work'] = get_work(document['UN_FSZN'])
    # if "UN_EDUCATION" in document:
    #     Log.logger.debug(get_education(document['UN_EDUCATION']))
    #     new_document['Education'] = get_education(document['UN_EDUCATION'])
    if "UN_ADDRESS" in document:
        Log.logger.debug(get_address(document['UN_ADDRESS']))
        new_document['Address'] = get_address(document['UN_ADDRESS'])
    return new_document


def get_work(document):
    """
    парсим работы по человеку
    :param document: массив (в идеале) объектов работ
    :return: строку неробходимой структуры
    """
    new_document = []
    if isinstance(document, list):
        for x in document:
            Log.logger.debug(x)
            new_document.append(get_work_by_element(x))
    elif isinstance(document, dict):
        new_document.append(get_work_by_element(document))
    Log.logger.info(new_document)
    return new_document

def get_work_by_element(document):
    """
    отрабатываем работу по одной
    :param document: словарь по работе
    :return: обновленная структура
    """
    return {'Organization': OracleUtils.get_work(document['FSZN_UNN']), 'start': document['FSZN_BEGIN_DATE'],
            'finish': document['FSZN_END_DATE']}

def get_education(document):
    """
    парсим образование по человеку
    :param document: массив (в идеале) объектов работ
    :return: строку неробходимой структуры
    """
    new_document = []
    Log.logger.debug(document)
    if isinstance(document, list):
        for x in document:
            Log.logger.debug(x)
            new_document.append(get_education_by_element(x))
    elif isinstance(document, dict):
        new_document.append(get_education_by_element(document))
    Log.logger.info(new_document)
    return new_document

def get_education_by_element(document):
    """
    отрабатываем образование по одному
    :param document: словарь по образованию
    :return: обновленная структура
    """
    return {'University': document['LEX_EDUCATION_ORGAN'], 'Spetiality': document['LEX_SPECIALIZATION'],
            'finish': document['EDUCATION_END_DATE']}


def get_address(document):
    """
    парсим образование по человеку
    :param document: массив (в идеале) объектов работ
    :return: строку неробходимой структуры
    """
    new_document = []
    if isinstance(document, list):
        for x in document:
            new_document.append(get_address_by_element(x))
    elif isinstance(document, dict):
        new_document.append(get_address_by_element(document))
    return new_document

def get_address_by_element(document):
    """
    отрабатываем образование по одному
    :param document: словарь по образованию
    :return: обновленная структура
    """
    result_document = {}
    if document['LEX_AREA_L'] is not None:
        result_document['Area'] = document['LEX_AREA_L'] + ' область'
    if document['LEX_REGION_L'] is not None:
        result_document['Region'] = document['LEX_REGION_L'] + ' район'
    if document['LEX_TYPE_CITY_L'] is not None:
        result_document['City'] = document['LEX_TYPE_CITY_L'] + document['LEX_CITY_L']
    if document['LEX_TYPE_STREET_L'] is not None:
        result_document['Street'] = document['LEX_TYPE_STREET_L'] +' ' + document['LEX_STREET_L']
    if document['HOUSE'] is not None:
        temp = document['HOUSE']
        if document['KORPS'] is not None:
            temp = temp+'-'+document['KORPS']
        result_document['House'] =temp
    if document['APP'] is not None:
        result_document['Apartment'] = document['APP']

    return result_document


def repl_str(area, region, city_type, city):
    """
    собираем адрес в одну строку
    :param area:  область
    :param region:  район
    :param city_type: тип населенного пункта
    :param city: наименование населенного пункта
    :return: собранная стрпуктура
    """
    res_str = ''
    if area is not None:
        res_str = area.capitalize()

    if region is not None:
        if len(res_str) > 0:
            res_str = res_str + ', ' + region.capitalize() + ' район'
        else:
            res_str = region.capitalize() + ' район'
    if city_type is not None:
        if len(res_str) > 0:
            res_str = res_str + ', ' + city_type.lower() + '. '
        else:
            res_str = city_type.lower() + '. '
    if city is not None:
        res_str = res_str + city.capitalize()
    return res_str


def init_cap(in_val):
    """
     капиталайзим строку
    :param in_val: входная строка
    :return: выходна строка
    """
    if in_val is not None:
        return in_val.capitalize()
    else:
        return ''
