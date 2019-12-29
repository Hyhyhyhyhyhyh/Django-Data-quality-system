import sys,MySQLdb
sys.path.insert(0, '..')
from mysite import db_config

def query_progressbar(company, quarter):
    try:
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        sql  = "select count(*) from check_result_{0}_{1} where check_sql is not null and check_sql != '' ".format(company,quarter)
        curs.execute(sql)
        for i in curs.fetchone():
            to_be_check_cnt = i
            
        sql  = "select count(*) from check_result_{0}_{1} where check_sql is not null and check_sql != '' and update_flag='Y'".format(company,quarter)
        curs.execute(sql)
        for i in curs.fetchone():
            checked_cnt = i
        
        curs.close()
        conn.close()
        value = round(checked_cnt/to_be_check_cnt*100,2)
        return value
    except Exception:
        return 0