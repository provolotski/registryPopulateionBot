import xmltodict
import logging
import MongoUtils
import OracleUtils

# {'ID', 'UN_DOCS', 'LEX_TYPE_CITY_B', 'SURNAME_BEL', 'IDENTIF', 'UN_INSURANCE', 'LEX_CITIZENSHIP',
# 'UN_SALARY', 'SID', 'AREA_B', 'UN_ADDRESS_TEMP', 'UN_COURT4', 'UN_PENSION', 'NAME_BEL', 'UN_COURT2',
# 'UN_SCIENCE_DEGREE', 'NAME', 'C_SEX', 'SURNAME', '@ID', 'C_CITIZENSHIP', 'REGION_B', 'SNAME_BEL',
# 'T_SEX', 'UN_FSZN', 'T_COUNTRY_B', 'UN_COURT3', 'C_COUNTRY_B', 'UN_EDUCATION', 'UN_FAMILY', 'SNAME',
# 'UN_UNEMPLOYMENT', 'C_TYPE_CITY_B', 'BIRTH_DATE', 'LEX_SEX', 'UN_ADDRESS', 'T_CITIZENSHIP', 'CITY_B',
# 'UN_SCIENCE_RANG', 'LEX_COUNTRY_B', 'T_TYPE_CITY_B'}

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

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
    logger.info('file uploaded')
    client = MongoUtils.get_database()
    logger.info('connected to nongo')
    for person in tree.findall('UN_PERSON'):
        o = (xmltodict.parse(etree.tostring(person)))
        o1 = generate_new_structure(o['UN_PERSON'])
        id = MongoUtils.insert_document(client, o1)
        logger.info('Загружен пользователь %s ', )


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
    if "UN_FSZN" in document:
        new_document['Work'] = get_work(document['UN_FSZN'])
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
            logger.debug(x)
            new_document.append(get_work_by_element(x))
    elif isinstance(document, dict):
        new_document.append(get_work_by_element(document))
    logger.info(new_document)
    return new_document


def get_work_by_element(document):
    """
    отрабатываем работу по одной
    :param document: словарь по работе
    :return: обновленная структура
    """
    return {'Organization': OracleUtils.get_work(document['FSZN_UNN']), 'start': document['FSZN_BEGIN_DATE'],
            'finish': document['FSZN_END_DATE']}


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
