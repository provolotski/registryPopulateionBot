import logging

import cx_Oracle

dsn_tns = cx_Oracle.makedsn('ip', 'port',
                            service_name='sid')
try:
    conn = cx_Oracle.connect(user=r'user', password='password',
                         dsn=dsn_tns)
except:
    logging.critical('No Oracle connection')


def connect_db():
    c = conn.cursor()
    c.execute('select * from dual')
    return c.fetchone()[0]


def get_work(p_id):
    try:
        c = conn.cursor()
        sql = "select varc_data from SS_METADATA.ESN_ITEM ei, SS_METADATA.ESN_HISTORY_CV ehc where ei.code_esni_unp =:unp  " \
            "and ei.id_esni = ehc.id_esni and ei.end_date_esni = ehc.end_date_esnhcv and ehc.id_esnc=84 union all select :unp as varc_data from dual"
        c.execute(sql, [p_id])
        return c.fetchone()[0]
    except:
        return p_id
    # except
#    conn.close()
