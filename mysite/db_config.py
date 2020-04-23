import MySQLdb
from sqlalchemy import create_engine


mysql_host    = '127.0.0.1'
mysql_port    = 3306
conn_user     = 'system'
conn_password = 'H5cT7yHB8_'
database      = 'data_quality'
conn_charset  = 'utf8mb4'
socket        = '/var/lib/mysql/mysql.sock'
    
    
def mysql_connect():
    conn = MySQLdb.connect(host=mysql_host,
                           port=mysql_port,
                           user=conn_user,
                           passwd=conn_password,
                           db=database,
                           charset=conn_charset,
                           unix_socket=socket,
                           use_unicode=True)
    return conn


def sqlalchemy_conn():
    engine = create_engine(
        f'mysql+mysqldb://{conn_user}:{conn_password}@{mysql_host}/{database}?charset={conn_charset}&unix_socket={socket}',
        echo=False,                     # 打印sql语句
        max_overflow=0,                 # 超过连接池大小外最多创建的连接
        pool_size=5,                    # 连接池大小
        pool_timeout=30,                # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1,                # 多久之后对线程池中的线程进行一次连接的回收（重置）
    )
    return engine