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