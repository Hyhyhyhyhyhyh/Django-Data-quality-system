import datetime
import math
import sys

from crontab import CronTab
from django.shortcuts import render

sys.path.insert(0, '..')
from mysite import db_config
from utils import functions as f
from utils.functions import is_login


@is_login
def rule_list(request):
    """
    检核规则列表
    :param request:
    :return:
    """
    return render(request, "check/rule_list.html", {"source_system": request.GET.get('company'),
                                                    "risk_market_filter": request.GET.get('risk_market'),
                                                    "username": request.session['username']
                                                    }
                  )


@is_login
def rule_edit(request):
    """
    单条检核规则页面
    :param request:
    :return:
    """
    return render(request, "check/rule_edit.html", {"username": request.session['username'],
                                                   "source_system": request.GET.get('company'),
                                                   "id": request.GET.get('id')
                                                   })


@is_login
def rule_execute_manual(request):
    """
    查询检核进度
    :param request:
    :return:
    """
    date = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + '-' + str(datetime.datetime.now().day)
    return render(request, "check/rule_exec.html", {"date": date})


@is_login
def show_crontab(request):
    """
    自动检核配置页面
    :param request:
    :return:
    """
    conn = db_config.mysql_connect()
    with conn.cursor() as curs:
        # 查询各个公司检核规则配置的数据库、上次检核任务的运行情况
        sql = """select distinct b.name,
                                a.company,
                                a.db,
                                CAST(c.execute_date as char),
                                c.status
                from check_result_template a,
                source_db_info b,
                (select db,company,execute_date,status from check_execute_log  where id in 
                    (
                        select id from (select max(id) id,company,db from check_execute_log where db is not null group by company,db) a
                    )
                ) c
                where a.db=b.alias
                and a.db=c.db
                and a.company=c.company
                order by 1,2,3"""
        curs.execute(sql)
        jobs = curs.fetchall()
        
    # 根据数据源中的公司和数据库信息匹配crontab定时任务
    cron = CronTab(user=True)
    data = []
    for i in jobs:
        job = list(cron.find_comment(f'autocheck-{i[1]}-{i[2]}'))
        t = list(i)
        if len(job) > 0:
            enable = job[0].is_enabled()                                # 获取crontab启用状态
            job_time = job[0].description(use_24hour_time_format=True, locale_code='zh_CN') # 获取crontab的调度周期 
            t.extend([enable, job_time])
        else:
            t.append(None)
        data.append(t)
    
    return render(request, "check/crontab.html", {"jobs": data})


@is_login
def blood_analyze(request):
    """血缘分析"""
    return render(request, "check/blood_analyze.html") 