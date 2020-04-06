import MySQLdb
import pymssql
import cx_Oracle
import os

# SQL server数据库
def sqlserver_db():
    conn = pymssql.connect(host='',
                           user='',
                           password='',
                           database='',
                           charset='utf8'
                           )
    return conn

# Oracle数据库
def oracle_db():
    os.environ['NLS_LANG']    = 'AMERICAN_AMERICA.UTF8'
    os.environ['ORACLE_HOME'] = ''
    conn = cx_Oracle.connect('')
    return conn

# MySQL数据库
def mysql_db():
    conn = MySQLdb.connect(host='',
                           port='',
                           user='',
                           passwd='',
                           db='',
                           charset='utf8',
                           use_unicode=True
                           )
    return conn
