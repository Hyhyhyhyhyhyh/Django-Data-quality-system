from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
import datetime, math

import sys, MySQLdb
sys.path.insert(0, '..')
from mysite import db_config

from utils import query
from check.autocheck import Check, MyThread
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


#修改检核规则状态，禁用/启用 规则的状态
def rule_status_modify(request):
    id = request.POST.get('id')
    post_status = request.POST.get('status')
    company = request.POST.get('company')

    conn = db_config.mysql_connect()
    curs = conn.cursor()
    curs.execute('set autocommit=0')
    #修改状态
    try:
        if post_status == '已启用':
            sql = f"update check_result_template set status='已停用' where id={id} and source_system='{company}'"
            rr = curs.execute(sql)
            conn.commit()
            return JsonResponse({'msg': '修改成功', 'code': 1000})
        else:
            sql = f"update check_result_template set status='已启用' where id={id} and source_system='{company}'"
            rr = curs.execute(sql)
            conn.commit()
            return JsonResponse({'msg': '修改成功', 'code': 1000})
    except:
        return HttpResponse('error', status=500)
    finally:
        curs.close()
        conn.close()


# --------------------------------------------------------------------------------------------------------------------------------
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
    try:
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        # 判断是否已经检核过，检核过则查询进度，未检核过则显示0
        sql = f"select count(table_name) from information_schema.tables where table_name like 'check_result_%_{quarter}%'"
        curs.execute(sql)
        if_checked = [i for i in curs.fetchone()]

        if if_checked == 0:
            progressbar = [0, 0, 0, 0, 0, 0, 0]
        else:
            for company in ('xt', 'zc', 'db', 'jk', 'jj1', 'jj2', 'jz'):
                progressbar.append(query.query_check_progressbar(company, quarter))
        curs.close()
        conn.close()
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
    except:
        return HttpResponse('error', status=500) 


################################################    以下是ajax POST请求的函数    ################################################


#获取检核规则详情，前端ajax调用
def rule_detail(request):
    company = request.GET.get('name')
    filter = request.GET.get('risk_market_filter')

    conn = db_config.mysql_connect()
    curs = conn.cursor()
    curs.execute('set autocommit=0')
    try:
        sql = f"select id,check_item,target_table,risk_market_item,problem_type,db,check_sql,note,status,source_system from check_result_template where source_system in ('{company}') and risk_market_item like '%{filter}%' order by id"
        curs.execute(sql)
        result = curs.fetchall()
        #构造json
        result_list = []
        for i in result:
            result_dict = {}
            result_dict["id"]               = i[0]
            result_dict["check_item"]       = i[1]
            result_dict["target_table"]     = i[2]
            result_dict["risk_market_item"] = i[3]
            result_dict["problem_type"]     = i[4]
            result_dict["db"]               = i[5]
            result_dict["check_sql"]        = i[6]
            result_dict["note"]             = i[7]
            result_dict["status"]           = i[8]
            result_dict["source_system"]    = i[9]
            result_list.append(result_dict)
        json_data = {'data': result_list}
        return JsonResponse(json_data)
    except:
        return HttpResponse('error', status=500)
    finally:
        curs.close()
        conn.close()


#执行修改检核规则，前端ajax调用
def rule_update(request):
    id              = request.POST.get('id')
    source_system   = request.POST.get('source_system')
    check_item      = request.POST.get('check_item')
    target_table    = request.POST.get('target_table')
    risk_market     = request.POST.get('risk_market')
    problem_type    = request.POST.get('problem_type')
    db              = request.POST.get('db')
    check_sql       = request.POST.get('code')
    note            = request.POST.get('note')
    status          = request.POST.get('status')
    
    #把"转义为'，再把'转义为''
    check_sql = MySQLdb.escape_string(check_sql).decode('utf-8')
    #print(check_sql)
    try:
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')
        sql = f"""update check_result_template set check_item='{check_item}',
                                                target_table='{target_table}',
                                                risk_market_item='{risk_market}',
                                                problem_type='{problem_type}',
                                                db='{db}',
                                                check_sql='{check_sql}',
                                                note='{note}',
                                                status='{status}'
                                                where id={id} and source_system='{source_system}'"""
        # print(sql)
        curs.execute(sql)
        conn.commit()
        return JsonResponse({'msg': '修改成功', 'code': 1000})
    except Exception as e:
        return HttpResponse(e, status=500)
    finally:
        curs.close()
        conn.close()


#执行新增检核规则，前端ajax调用
def rule_add(request):
    source_system   = request.POST.get('source_system')
    check_item      = request.POST.get('check_item')
    target_table    = request.POST.get('target_table')
    risk_market     = request.POST.get('risk_market')
    problem_type    = request.POST.get('problem_type')
    db              = request.POST.get('db')
    code            = request.POST.get('code')
    note            = request.POST.get('note')
    status          = request.POST.get('status')
    
    #处理检核SQL中含有''的情况
    check_sql = MySQLdb.escape_string(code).decode('utf-8')
    # print(check_sql)
    try:
        #连接数据库
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')
        sql = "select max(id)+1 from check_result_template where source_system in ('" + source_system + "')"
        curs.execute(sql)
        result = curs.fetchone()
        new_id = str(result[0])  #获取新增的id
        sql = f"""insert into check_result_template(id,
                                                    source_system,
                                                    check_item,
                                                    target_table,
                                                    risk_market_item,
                                                    problem_type,
                                                    db,
                                                    check_sql,
                                                    note,
                                                    status)
                values({new_id},
                        '{source_system}',
                        '{check_item}',
                        '{target_table}',
                        '{risk_market}',
                        '{problem_type}',
                        '{db}',
                        '{check_sql}',
                        '{note}',
                        '{status}')"""
        # print(sql)
        curs.execute(sql)
        conn.commit()
        return JsonResponse({'msg': '修改成功', 'code': 1000})
    except Exception as e:
        return HttpResponse(e, status=500)
    finally:
        curs.close()
        conn.close()


# 执行检核，前端ajax调用
def rule_execute(request):
    company  = request.POST.get('company')
    username = request.POST.get('username')
    quarter  = request.POST.get('quarter')

    if company == 'xt':
        check = Check()
        if check.init_table(company, source_system, quarter):
            # 初始化3个线程
            thread1 = MyThread(func=check.run_check,
                               args=(company, source_system, quarter,'oracle'))
            thread2 = MyThread(func=check.run_check,
                               args=(company, source_system, quarter,'sqlserver'))
            thread3 = MyThread(func=check.xt_spec, args=(quarter, ))
            thread4 = MyThread(func=check.run_check,
                               args=(company, source_system, quarter, 'mysql'))
            #开启3个线程
            thread1.start()
            thread2.start()
            thread3.start()
            thread4.start()
            # 等待运行结束
            thread1.join()
            thread2.join()
            thread3.join()
            thread4.join()

            if thread1.get_result() is True:
                if thread2.get_result() is True:
                    if thread3.get_result() is True:
                        if thread4.get_result() is True:
                            run = True
                        else:
                            return JsonResponse({
                                "status":
                                "检核过程发生错误：" + str(thread4.get_result())
                            })
                    else:
                        return JsonResponse({
                            "status":
                            "检核过程发生错误：" + str(thread3.get_result())
                        })
                else:
                    return JsonResponse(
                        {"status": "检核过程发生错误：" + str(thread2.get_result())})
            else:
                return JsonResponse(
                    {"status": "检核过程发生错误：" + str(thread1.get_result())})
        else:
            return JsonResponse({"status": "初始化检核表发生错误"})

    elif company == 'zc':
        source_system = '资产'
        check = Check()
        if check.init_table(company, source_system, quarter):
            run = check.run_check(company, source_system, quarter, None)
            if run is not True:
                return JsonResponse({"status": "检核过程发生错误：" + str(run)})
        else:
            return JsonResponse({"status": "初始化检核表发生错误"})

    elif company == 'db':
        source_system = '担保'
        check = Check()
        if check.init_table(company, source_system, quarter):
            run = check.run_check(company, source_system, quarter, None)
            if run is not True:
                return JsonResponse({"status": "检核过程发生错误：" + str(run)})
        else:
            return JsonResponse({"status": "初始化检核表发生错误"})

    elif company == 'jk':
        source_system = '金科'
        check = Check()
        if check.init_table(company, source_system, quarter):
            run = check.run_check(company, source_system, quarter, None)
            if run is not True:
                return JsonResponse({"status": "检核过程发生错误：" + str(run)})
        else:
            return JsonResponse({"status": "初始化检核表发生错误"})

    elif company == 'jj1':
        source_system = '基金1'
        check = Check()
        if check.init_table(company, source_system, quarter):
            run = check.run_check(company, source_system, quarter, None)
            if run is not True:
                return JsonResponse({"status": "检核过程发生错误：" + str(run)})
        else:
            return JsonResponse({"status": "初始化检核表发生错误"})

    elif company == 'jj2':
        source_system = '基金2'
        check = Check()
        if check.init_table(company, source_system, quarter):
            run = check.run_check(company, source_system, quarter, None)
            if run is not True:
                return JsonResponse({"status": "检核过程发生错误：" + str(run)})
        else:
            return JsonResponse({"status": "初始化检核表发生错误"})

    elif company == 'jz':
        source_system = '金租'
        check = Check()
        if check.init_table(company, source_system, quarter):
            run = check.run_check(company, source_system, quarter, None)
            if run is not True:
                return JsonResponse({"status": "检核过程发生错误：" + str(run)})
        else:
            return JsonResponse({"status": "初始化检核表发生错误"})

    if run == True:
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')
        sql = "insert into check_execute_log values(null,'{0}','{1}',now(),'{2}')".format(
            quarter, company, username)
        print(sql)
        curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
        return JsonResponse({
            "status": "success",
            "msg": source_system + "公司检核成功！"
        })
