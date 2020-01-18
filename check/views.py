from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
import datetime, math

import sys, MySQLdb
sys.path.insert(0, '..')
from mysite import db_config

from utils import query
from utils.functions import is_login


#检核规则列表
@is_login
def rule_list(request):
    username = request.session['username']
    company = request.GET.get('name')
    filter = request.GET.get('risk_market')
    return render(
        request, "check/rule_list.html", {
            "username": username,
            "source_system": company,
            "risk_market_filter": filter
        })


#单条检核规则页面
@is_login
def rule_config(request):
    username = request.session['username']
    company = request.GET.get('company')
    id = request.GET.get('id')
    if id != 'null':  #POST传过来的id非空，进行“检核规则编辑”
        #连接数据库
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')
        sql = f"select id,check_item,target_table,risk_market_item,problem_type,db,check_sql,note,status from check_result_template where source_system in ('{company}') and id={id}"
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
        return render(
            request, "check/rule_config.html", {
                "username": username,
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
            })
    else:  #POST传过来的id为空，进行“检核规则新增”
        return render(request, "check/rule_add.html", {
            "username": username,
            "source_system": company
        })


# 执行检核结果页面
@is_login
def rule_exec(request):
    username = request.session['username']
    quarter = query.get_user_quarter(request)
    
    conn = db_config.mysql_connect()
    curs = conn.cursor()
    try:
        # 判断是否已经检核过，检核过则查询进度，未检核过则显示0
        sql = f"select count(table_name) from information_schema.tables where table_name like 'check_result_%_{quarter}%'"
        curs.execute(sql)
        if_checked = [i for i in curs.fetchone()]
        if if_checked == 0:
            progressbar = [0, 0, 0, 0, 0, 0, 0]
        else:
            progressbar = []
            for company in ('xt', 'zc', 'db', 'jk', 'jj1', 'jj2', 'jz'):
                progressbar.append(query.query_check_progressbar(company, quarter))
        
        return render(
            request, "check/rule_exec.html", {
                "username": username,
                "quarter": quarter,
                "progressbar_xt":  progressbar[0],
                "progressbar_zc":  progressbar[1],
                "progressbar_db":  progressbar[2],
                "progressbar_jk":  progressbar[3],
                "progressbar_jj1": progressbar[4],
                "progressbar_jj2": progressbar[5],
                "progressbar_jz":  progressbar[6]
            })
    except Exception as e:
        print(e)
        return HttpResponse('error', status=500)
    finally:
        curs.close()
        conn.close()