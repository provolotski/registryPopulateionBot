import Util.log as log
import Util.config as config
import cx_Oracle


def get_connection():
    dsn_tns = cx_Oracle.makedsn(config.ORACLE_HOST, config.ORACLE_PORT,
                                service_name=config.ORACLE_SID)
    try:
        conn = cx_Oracle.connect(user=config.ORACLE_USER, password=config.ORACLE_PASSWORD,
                                 dsn=dsn_tns)
        return conn
    except Exception as e:
        log.logging.critical('No Oracle connection')
        log.logger.critical('Failed to connect to database: ' + str(e))


def connect_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select * from dual')
    return cursor.fetchone()[0]


def get_work(p_id):
    try:
        try:
            conn = get_connection()
            c = conn.cursor()
        except:
            log.logging.critical('not connected')
        sql = "select varc_data from SS_METADATA.ESN_ITEM ei, SS_METADATA.ESN_HISTORY_CV ehc where ei.code_esni_unp =:unp  " \
              "and ei.id_esni = ehc.id_esni and ei.end_date_esni = ehc.end_date_esnhcv and ehc.id_esnc=84"
        c.execute(sql, [p_id])
        return c.fetchone()[0]
    except:
        return p_id

