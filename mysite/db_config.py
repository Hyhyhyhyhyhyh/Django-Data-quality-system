import MySQLdb

def mysql_connect():
    mysql_host    = '127.0.0.1'
    mysql_port    = 3306
    conn_user     = 'system'
    conn_password = 'H5cT7yHB8_'
    database      = 'data_quality'
    conn_charset  = 'utf8'
    socket        = '/var/lib/mysql/mysql.sock'
    conn = MySQLdb.connect(host=mysql_host,
                           port=mysql_port,
                           user=conn_user,
                           passwd=conn_password,
                           db=database,
                           charset=conn_charset,
                           unix_socket=socket,
                           use_unicode=True)
    return conn
