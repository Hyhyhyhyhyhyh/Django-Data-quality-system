import sys, MySQLdb, logging, threading
sys.path.insert(0, '..')
from mysite import db_config, source_db_config

class Check(object):
    def init_table(self, company, source_system, quarter):
        '''
        类实例化所需参数
            company: 公司名
            source_system: 源系统名称
            quarter: 季度
        
        初始化检核表
            如果check_result_{0}_{1}表存在，则truncate数据后从check_result_template表中插入对应公司检核项和逻辑
            如果check_result_{0}_{1}表不存在，则使用check_result_template表作为模板新建
        '''
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",  # 日志的格式
            datefmt=" %Y-%m-%d %H:%M:%S",                                                  # 时间格式
            filename="/data/pyweb/data-quality/logs/check.log",                                       # 指定文件位置
            filemode="a",
        )
        logging.info("初始化"+source_system+"检核表..."+quarter)
        
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        sql  = "select table_name from information_schema.tables where table_schema='data_quality' and table_name='check_result_{0}_{1}'".format(company, quarter)
        table_count = curs.execute(sql)
        if table_count == 1:
            sql = "truncate table check_result_{0}_{1}".format(company, quarter)
            curs.execute(sql)
            sql = "insert into check_result_{0}_{1} select * from check_result_template where source_system in('{2}') order by id".format(company, quarter, source_system)
            curs.execute(sql)
            conn.commit()
        elif table_count == 0:
            sql  = "create table check_result_{0}_{1} as select * from check_result_template where source_system in('{2}') order by id".format(company, quarter, source_system)
            curs.execute(sql)
        else:
            curs.close()
            conn.close()
            logging.error("初始化"+source_system+"检核表"+quarter+"...失败")
            return False
        curs.close()
        conn.close()
        logging.info("初始化"+source_system+"检核表"+quarter+"...完成")
        return True
    
    def run_check(self, company, source_system, quarter, db):
        '''执行检核
        类实例化所需参数
            company: 公司名
            quarter: 要更新记录的季度名
            source_system: 源系统名称
            db: 检核的数据库
        '''
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",  # 日志的格式
            datefmt=" %Y-%m-%d %H:%M:%S",                                                  # 时间格式
            filename="/data/pyweb/data-quality/logs/check.log",                                       # 指定文件位置
            filemode="a",
        )
        logging.info("正在检核"+source_system+"数据..."+quarter)
        
        try:
            conn = db_config.mysql_connect()
            curs = conn.cursor()
            curs.execute('set autocommit=0')
            
            if db is not None:
                sql = "select id,check_sql from check_result_template where source_system='{0}' and check_sql is not null and check_sql != '' and db='{1}' order by id".format(source_system, db)
            else:
                sql = "select id,check_sql from check_result_template where source_system='{0}' and check_sql is not null and check_sql != '' order by id".format(source_system, db)
            curs.execute(sql)
            check_list = curs.fetchall()

            '''
            if company == '' and db == '':
                conn_source = source_db_config.xxx_db()
                curs_source = conn_source.cursor()
            '''
            conn_source = None
            curs_source = None
             
            for i in check_list:
                id = i[0]
                check_sql = i[1]
                logging.info(source_system + str(i[0]) + "...开始检核")
                curs_source.execute(check_sql)
                check_result = curs_source.fetchall()    #检核结果
                for t in check_result:
                    item_count    = t[0]
                    problem_count = t[1]
                    archive_sql   = "update check_result_{0}_{1} set item_count={2} ,problem_count={3}, update_flag='Y' where id={4}".format(company, quarter, item_count, problem_count, id)
                    curs.execute(archive_sql)
                    conn.commit()
                logging.info(source_system + str(i[0])+"...完成")
            curs_source.close()
            conn_source.close()
            
            #补全未创建项的[检核数据量]+[问题数据量]
            #使用[目标表]的最大行数更新未创建项的检核和问题行数
            sql = "select distinct target_table,item_count from check_result_{0}_{1} where item_count is not null".format(company, quarter)
            curs.execute(sql)
            for i in curs.fetchall():
                target_table = i[0]
                item_count   = i[1]
                sql = "update check_result_{0}_{1} set item_count={2},problem_count={2} where item_count is null and problem_count is null and target_table='{3}' and risk_market_item='是'".format(company, quarter, item_count, target_table)
                curs.execute(sql)
            
            ####  计算问题占比  #### 
            #处理item_count和problem_count都是null或=0的行
            sql = "update check_result_{0}_{1} set problem_per=100 where (item_count is null or item_count=0) and risk_market_item='是'".format(company, quarter)
            curs.execute(sql)
            
            #计算正常的问题占比
            sql = "update check_result_{0}_{1} set problem_per=problem_count/item_count*100 where risk_market_item='是'".format(company, quarter)
            curs.execute(sql)
            
            conn.commit()
            curs.close()
            conn.close()
            logging.info("**************************************")
            logging.info(source_system+"公司数据检核完成")
            logging.info("**************************************")
            return True
        except Exception as e:
            logging.error(source_system+"公司数据检核出错..." + str(e))
            return e
    

class MyThread(threading.Thread):
    """重新定义带返回值的线程类"""
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args
    def run(self):
        self.result = self.func(*self.args)
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None