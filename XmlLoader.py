import bson
import xmltodict
import Util.log as Log
import Databases


def get_xml(file_name):
    """
    отработка xml и занесение его mongo
    :param file_name: название файла
    """
    Log.logger.info(f'Работаем с файлом {file_name}')
    try:
        from lxml import etree
    except ImportError:
        import xml.etree.cElementTree as etree
    tree = etree.parse(file_name)
    Log.logger.info('file uploaded')
    client = Databases.MongoUtils.get_database()
    Log.logger.info('connected to Mongo')
    redis = Databases.RedisUtils.connect()
    Log.logger.info('connected to Redis')
    i = 0
    for person in tree.findall('UN_PERSON'):
        i += 1
        xml_object = (xmltodict.parse(etree.tostring(person)))
        new_object = generate_new_structure(xml_object['UN_PERSON'])
        mongo_document_id = Databases.MongoUtils.insert_document(client, new_object)
        redis.set(xml_object['UN_PERSON']['ID'], str(mongo_document_id))
        if 10000 != 0:
            continue
        Log.logger.info(f'Обработано {i} записей')
    Log.logger.info(f'По файлу {file_name} обработано {i} записей')


def generate_new_structure(document):
    """
    формируем запись по человеку
    :param document: входящий документ
    :return:
    """
    new_document = {'LastName': init_cap(document['SURNAME']), 'FirstName': init_cap(document['NAME']),
                    'MiddleName': init_cap(document['SNAME']), 'BirthDate': document['BIRTH_DATE'],
                    'BirthPlace': repl_str(document['AREA_B'], document['REGION_B'], document['LEX_TYPE_CITY_B'],
                                           document['CITY_B']), 'Sex': init_cap(document['LEX_SEX'])}
    if "UN_FSZN" in document:
        new_document['Work'] = get_work(document['UN_FSZN'])
    if "UN_EDUCATION" in document:
        new_document['Education'] = get_education(document['UN_EDUCATION'])
    if "UN_ADDRESS" in document:
        new_document['Address'] = get_address(document['UN_ADDRESS'])
    if "UN_FAMILY" in document:
        new_document['Family'] = get_family(document['UN_FAMILY'], document['LEX_SEX'])
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
            new_document.append(get_work_by_element(x))
    elif isinstance(document, dict):
        new_document.append(get_work_by_element(document))
    return new_document


def get_work_by_element(document):
    """
    отрабатываем работу по одной
    :param document: словарь по работе
    :return: обновленная структура
    """
    return {'Organization': Databases.OracleUtils.get_work(document['FSZN_UNN']), 'start': document['FSZN_BEGIN_DATE'],
            'finish': document['FSZN_END_DATE']}


def get_education(document):
    """
    парсим образование по человеку
    :param document: массив (в идеале) объектов работ
    :return: строку неробходимой структуры
    """
    new_document = []
    if isinstance(document, list):
        for x in document:
            new_document.append(get_education_by_element(x))
    elif isinstance(document, dict):
        new_document.append(get_education_by_element(document))
    return new_document


def get_education_by_element(document):
    """
    отрабатываем образование по одному
    :param document: словарь по образованию
    :return: обновленная структура
    """
    return {'University': document['LEX_EDUCATION_ORGAN'], 'Spetiality': document['LEX_SPECIALIZATION'],
            'finish': document['EDUCATION_END_DATE']}


def get_family(document, sex):
    """
    парсим образование по человеку
    :param document: массив (в идеале) объектов работ
    :return: строку неробходимой структуры
    """
    new_document = []
    if isinstance(document, list):
        for x in document:
            new_document.append(get_family_by_element(x, sex))
    elif isinstance(document, dict):
        new_document.append(get_family_by_element(document, sex))
    return new_document


def get_family_by_element(document, sex):
    """
    отрабатываем образование по одному
    :param document: словарь по образованию
    :return: обновленная структура
    """
    try:
        redis = Databases.RedisUtils.connect()
        value = redis.get(document['RELATIVE_ID'])
    except:
        value = None
    Log.logger.debug(f'value is {value}')
    result = {}
    if value is None:
        result['RelativeID'] = -1
        result['applic'] = document['RELATIVE_ID']
    else:
        result['RelativeID'] = bson.ObjectId(value.decode("utf-8"))
    result['relation'] = init_cap(document['RELATION']) if document[
                                                               'RELATION'] != 'СУПРУГ(А)' else 'Муж' if sex == 'ЖЕНСКИЙ' else 'Жена'
    return result


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
        return new_document
    elif isinstance(document, dict):
        return get_address_by_element(document)


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
        result_document['Street'] = document['LEX_TYPE_STREET_L'] + ' ' + document['LEX_STREET_L']
    if document['HOUSE'] is not None:
        temp = document['HOUSE']
        if document['KORPS'] is not None:
            temp = temp + '-' + document['KORPS']
        result_document['House'] = temp
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
    return ''
