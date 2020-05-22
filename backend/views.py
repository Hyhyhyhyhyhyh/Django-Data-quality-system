import re
import pandas as pd
from django.shortcuts import render
from django.http.response import HttpResponseBadRequest
from crontab import CronTab

from mysite import db_config
from utils.functions import is_login


@is_login
def database(request):
    """列出数据源
    """
    return render(request, "backend/database.html")


@is_login
def database_detail(request):
    """查看数据源详情
    """
    id = request.GET.get('id')
    
    try:
        conn = db_config.sqlalchemy_conn()
        db = pd.read_sql(f"select company,name,alias,ip,user,db,port,db_type,charset,note from source_db_info where id={id}", con=conn)
        return render(request, "backend/database_detail.html", {
                                                            'company': db['company'].values.tolist()[0],
                                                            'name': db['name'].values.tolist()[0],
                                                            'alias': db['alias'].values.tolist()[0],
                                                            'ip': db['ip'].values.tolist()[0],
                                                            'user': db['user'].values.tolist()[0],
                                                            'db': db['db'].values.tolist()[0],
                                                            'port': db['port'].values.tolist()[0],
                                                            'db_type': db['db_type'].values.tolist()[0],
                                                            'charset': db['charset'].values.tolist()[0],
                                                            'note': db['note'].values.tolist()[0],
                                                            'id': id
                                                        })
    except Exception as e:
        return HttpResponseBadRequest(content=e)
    finally:
        conn.dispose()


@is_login
def database_add(request):
    """新增数据源
    """
    return render(request, "backend/database_add.html")


@is_login
def crontab(request):
    """列出后台管理的定时任务
    """
    data = []
    cron = CronTab(user=True)
    job = list(cron.find_comment(re.compile(r'backend')))
    if job:
        for i in job:
            enable = i.is_enabled()
            job_time = i.description(use_24hour_time_format=True, locale_code='zh_CN') # 获取crontab的度周期
            comment = i.comment
            command = i.command
            data.append([comment, command, enable, job_time])
            return render(request, "backend/crontab.html", {"jobs": data})
    else:
        return render(request, "backend/crontab.html", {"jobs": None})
    