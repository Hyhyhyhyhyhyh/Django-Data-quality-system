#数据库连接配置，配置文件/data/pyweb/mysite/mysite/db_config.py
import sys, MySQLdb, math, datetime
sys.path.insert(0, '..')
from mysite import db_config
from itertools import chain
import numpy as np

def get_quarter_list():
# 获取检核结果库中所有季度的列表
     '''
# DDL:/data/pyweb/mysite/mysite/ddl.sql
     conn = db_config.mysql_connect()
     curs = conn.cursor()
     # 当一个季度的7家公司全部检核完，才会在下拉框中显示新季度出来
     sql  = "select distinct quarter from (select quarter,count(distinct company) as cnt from check_execute_log group by quarter) a where cnt>=7 order by quarter asc"
     curs.execute (sql)
     db_quarter_list = curs.fetchall()                            #此时的数据格式为二维元组(('2019Q1',), ('2019Q2',))
     quarter_list = list(chain.from_iterable(db_quarter_list))    #将二维元组转为一维元组，方便后续进行数据查询
     curs.close()
     conn.close()
     return quarter_list
     '''
     return ('2019Q1','2019Q2','2019Q3','2019Q4')

# 检核结果Excel明细
def get_result_detail(company, quarter):
     data = [
               [1, company, '项目编号', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [2, company, '项目名称', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [3, company, '项目类别', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [4, company, '项目投向行业', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [5, company, '项目投向（按功能）', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [6, company, '项目资金用途', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [7, company, '项目交易对手（投向）', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [8, company, '项目来源', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [9, company, '项目所在省', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [10, company, '项目所在市', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [11, company, '项目管理方式', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [12, company, '项目管理方式（监管）', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [13, company, '项目金额', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [14, company, '项目余额', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [15, company, '项目余额', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [16, company, '收益率', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [17, company, '风险等级', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
               [18, company, '资金或资产来源', '项目基本信息', '是', '控制检验', 'select col from tab', np.random.randint(5555,99999), np.random.randint(5555,99999), str(round(np.random.rand()*100, 2))+'%', None],
          ]

     return data


def query_check_progressbar(company, quarter):
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


# 初始化仪表盘季度
def get_user_quarter(request):
     '''
     传入参数：request
          如果GET请求没有传入quarter参数，则先判断用户session是否有上一次选定的季度
               - 如果上一次有选定季度，则显示上次选定的季度
               - 没有选定季度，则默认显示上一季度数据
          
     返回参数：quarter
     '''
     if request.GET.get('quarter') is None:
          if request.session.get('selected_quarter') is None:
               if math.ceil(datetime.datetime.now().month/3.)-1 == 0:      # 如果季度=0，则显示去年Q4季度
                    quarter = str(datetime.datetime.now().year-1) + "Q4"
               else:
                    quarter = str(datetime.datetime.now().year)+"Q"+str(math.ceil(datetime.datetime.now().month/3.)-1)
          else:
               quarter = request.session['selected_quarter']
     else:
          quarter = request.GET.get('quarter')
          request.session['selected_quarter'] = request.GET.get('quarter')
     return quarter