import logging
import sys
import threading
import os

sys.path.insert(0, '..')
from mysite import db_config
from utils import functions as f
from sqlalchemy import create_engine


os.environ['NLS_LANG']    = 'AMERICAN_AMERICA.UTF8'
os.environ['ORACLE_HOME'] = '/data/oracle/app/11.2.4'


class Check(object):
    def __init__(self, company):
        self.company = company
        
    def init_table(self):
        """
        类实例化所需参数
        :param company:         公司名
        :param source_system:   源系统名称
        :return:
        初始化检核表
            如果check_result_{0}表存在，则从check_result_template表中插入对应公司检核项和逻辑
            如果check_result_{0}表不存在，则使用check_result_template表作为模板新建
        """
        company = self.company
        
        logging.info('*' * 50)
        logging.info(f'开始初始化检核结果表...check_result_{company}')
        
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')
        
        sql = f"select table_name from information_schema.tables where table_schema='data_quality' and table_name='check_result_{company}'"
        table_count = curs.execute(sql)
        try:
            if table_count == 0:    # 表不存在则新建
                sql = f"""create table check_result_{company} as select * from check_result_template
                                                                where company='{company}' order by id,source_system"""
                curs.execute(sql)
            else:                   # 表存在则插入
                # 获取检核版本号
                curs.execute(f"select count(*) from check_execute_log where company='{company}'")
                version = curs.fetchone()[0] + 1
                # 可能存在了初始化完检核表，但是检核失败导致事务回滚，检核表check_version={version}数据项为空的情况，因此需要处理这种情况
                for sql in (
                    f"delete from check_result_{company} where check_version={version}",
                    f"insert into check_result_{company} select * from check_result_template where company='{company}' order by id,source_system",
                    f"update check_result_{company} set check_version={version} where check_version is null",
                ):
                    curs.execute(sql)
                
            conn.commit()
            logging.info('*' * 50, f"初始化 check_result_{company}表 ...完成", '*' * 50)
            return True
        except Exception as e:
            conn.rollback()
            logging.error('!' * 50, f'初始化 check_result_{company}表 ...失败,错误信息：{str(e)}', '!' * 50)
            return False
        finally:
            curs.close()
            conn.close()
    
    def run_check(self, db):
        """
        执行检核
        类实例化所需参数
        :param company: 公司简称
        :param db:      检核的数据库
        :return:
        """
        company = self.company
        
        logging.info('-' * 50)
        logging.info("正在检核" + company + "数据...")

        try:
            conn = db_config.mysql_connect()
            curs = conn.cursor()
            curs.execute('set autocommit=0')

            # 从规则库表中取出检核项和检核sql，只运行“已启用”状态的SQL
            sql = f"""select id,check_sql from check_result_template
                    where company='{company}'
                    and check_sql is not null
                    and check_sql != ''
                    and db='{db}'
                    and status='已启用'
                    order by id"""
            curs.execute(sql)
            check_list = curs.fetchall()
            
            
            # 连接源系统数据库
            curs.execute(f"select connection_string from source_db_info where company='{company}' and alias='{db}'")
            connection_string = curs.fetchone()[0]
            engine = create_engine(
                connection_string,
                echo=False,                     # 打印sql语句
                max_overflow=0,                 # 超过连接池大小外最多创建的连接
                pool_size=5,                    # 连接池大小
                pool_timeout=30,                # 池中没有线程最多等待的时间，否则报错
                pool_recycle=-1,                # 多久之后对线程池中的线程进行一次连接的回收（重置）
            )
            conn_source = engine.raw_connection()
            
            # 获取检核版本号
            curs.execute(f"select count(*) from check_execute_log where company='{company}'")
            version = curs.fetchone()[0] + 1

            with conn_source.cursor() as curs_source:
                # 执行检核
                for i in check_list:
                    id = i[0]
                    check_sql = i[1]
                    logging.info(f'{company}, db={db}, id={i[0]} >>>开始检核')
                    curs_source.execute(check_sql)
                    check_result = curs_source.fetchall()  # 检核结果
                    for t in check_result:
                        item_count = t[0]
                        problem_count = t[1]
                        archive_sql = f"""update check_result_{company}
                                            set item_count={item_count},
                                            problem_count={problem_count},
                                            update_flag='Y',
                                            check_date=current_timestamp
                                            where id={id}
                                            and check_version={version}"""
                        curs.execute(archive_sql)
                        conn.commit()
                    logging.info(f'{company}, db={db}, id={i[0]} <<<完成')
            conn_source.close()

            # 根据检核结果明细计算问题占比
            self.calc_result(version)
            
            logging.info("-" * 25, f'{company}, db={db} 检核完成', "-" * 25)
            return True
        except Exception as e:
            conn.rollback()
            logging.error("!" * 25, f'{company}, db={db}, id={id} 检核出错,错误信息：{str(e)}', "!" * 25)
            return False
        finally:
            curs.close()
            conn.close()
            
    def calc_result(self, version):
        """根据检核结果明细计算问题占比
        1. 填充空值的问题占比
        2. 计算正常的问题占比
        
        :param version:     要进行计算的版本号
        :return:            检核成功返回True，失败返回False
        """
        company = self.company
        try:
            conn = db_config.mysql_connect()
            curs = conn.cursor()
            curs.execute('set autocommit=0')
            # 计算问题占比
            # 处理item_count和problem_count都是null或=0的行
            sql = f"""update check_result_{company}
                        set problem_per=100
                        where (item_count is null or item_count=0)
                        and check_version={version}"""
            curs.execute(sql)

            # 计算正常的问题占比
            sql = f"""update check_result_{company} set problem_per=problem_count/item_count*100\
                        where problem_per is null
                        and check_version={version}"""
            curs.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            curs.close()
            conn.close()
    

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