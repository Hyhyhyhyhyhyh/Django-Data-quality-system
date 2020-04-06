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
                                                    "risk_market_filter": request.GET.get('risk_market')
                                                    }
                  )


@is_login
def rule_config(request):
    """
    单条检核规则页面
    :param request:
    :return:
    """
    username = request.session['username']
    company = request.GET.get('company')
    id = request.GET.get('id')

    if id != 'null':  # POST传过来的id非空，进行“检核规则编辑”
        # 连接数据库
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')
        sql = f"""select id,check_item,target_table,risk_market_item,problem_type,db,check_sql,note,status
from check_result_template
where source_system in ('{company}') and id={id}"""
        curs.execute(sql)
        result = curs.fetchall()
        for i in result:
            id = i[0]
            check_item = i[1]
            target_table = i[2]
            risk_market_item = i[3]
            problem_type = i[4]
            db = i[5]
            check_sql = i[6]
            note = i[7]
            status = i[8]
        curs.close()
        conn.close()
        return render(request, "check/rule_config.html", {"username": username,
                                                          "id": id,
                                                          "source_system": company,
                                                          "check_item": check_item,
                                                          "target_table": target_table,
                                                          "risk_market_item": risk_market_item,
                                                          "problem_type": problem_type,
                                                          "db": db,
                                                          "check_sql": check_sql,
                                                          "note": note,
                                                          "status": status,
                                                          }
                      )
    else:
        # POST传过来的id为空，进行“检核规则新增”
        return render(request, "check/rule_add.html", {"username": username, "source_system": company})


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
    cron = CronTab(user=True)
    job = list(cron.find_comment('自动进行数据质量检核'))[0]  # 根据comment查询crontab
    if job.is_enabled() is True:
        job_time = str(job).split('#')[0][0:9]
    else:
        job_time = str(job).split('#')[1][1:10]
    return render(request, "check/show_crontab.html", {"status": str(job.is_enabled()),
                                                       "job_name": job.comment,
                                                       "job_command": job.command,
                                                       "job_time": job_time,
                                                       "last_run": str(job.last_run),
                                                       }
                  )


@is_login
def blood_analyze(request):
    """血缘分析"""
    return render(request, "check/blood_analyze.html") 