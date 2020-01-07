#数据库连接配置，配置文件/data/pyweb/mysite/mysite/db_config.py
import sys,MySQLdb
sys.path.insert(0, '..')
from mysite import db_config
import numpy as np

def risk_market_total_count(quarter):
    return np.random.randint(5555, 99999)
    
def risk_market_problem_count(quarter):
    return np.random.randint(5555, 99999)
    
def risk_market_problem_detail(company, quarter):
    data = ['项目编号', '空值检验', np.random.randint(5555, 99999), np.random.randint(5555, 99999), str(round(np.random.rand()*100, 2))+'%', None]
    return data