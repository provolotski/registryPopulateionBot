import logging
import os

import cx_Oracle


def get_connection():
    dsn_tns = cx_Oracle.makedsn(os.environ['OracleHost'], os.environ['OraclePort'],
                            service_name=os.environ['OracleSid'])
    try:
        conn = cx_Oracle.connect(user=os.environ['OracleUser'], password=os.environ['OraclePassword'],
                         dsn=dsn_tns)
        return conn
    except:
        logging.critical('No Oracle connection')


def connect_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('select * from dual')
    return c.fetchone()[0]


def get_work(p_id):
    try:
        try:
            conn = get_connection()
            c = conn.cursor()
        except:
            logging.critical('not connected')
        sql = "select varc_data from SS_METADATA.ESN_ITEM ei, SS_METADATA.ESN_HISTORY_CV ehc where ei.code_esni_unp =:unp  " \
            "and ei.id_esni = ehc.id_esni and ei.end_date_esni = ehc.end_date_esnhcv and ehc.id_esnc=84"
        c.execute(sql, [p_id])
        return c.fetchone()[0]
    except:
        return p_id
    # except
#    conn.close()
