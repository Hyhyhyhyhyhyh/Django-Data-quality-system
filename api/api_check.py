from django.http.response import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from crontab import CronTab
import pandas as pd

import sys, MySQLdb

sys.path.insert(0, '..')
from mysite import db_config
from check.autocheck import Check, MyThread


@require_http_methods(['GET'])
def rule(request):
    """
    根据公司名查询所有检核规则详情
    """
    company = request.GET.get('name')
    filter = request.GET.get('risk_market_filter')

    conn = db_config.mysql_connect()
    curs = conn.cursor()
    curs.execute('set autocommit=0')
    try:
        sql = f"""select id,check_item,target_table,risk_market_item,problem_type,db,check_sql,note,status,source_system
                    from check_result_template
                    where source_system in ('{company}')
                    and risk_market_item like '%{filter}%'
                    order by id"""
        curs.execute(sql)
        result = curs.fetchall()
        # 构造json
        result_list = []
        for i in result:
            result_dict = {"id": i[0], "check_item": i[1], "target_table": i[2], "risk_market_item": i[3],
                           "problem_type": i[4], "db": i[5], "check_sql": i[6], "note": i[7], "status": i[8],
                           "source_system": i[9]}
            result_list.append(result_dict)
        json_data = {'data': result_list}
        return JsonResponse(json_data)
    except:
        return HttpResponse('error', status=500)
    finally:
        curs.close()
        conn.close()
        
        
@require_http_methods(['GET'])
def rule_detail(request):
    """
    根据公司名、id查询单条规则详情
    """
    company = request.GET.get('company')
    id =  request.GET.get('id')
    
    data = {
        "id": None,
        "source_system": None,
        "check_item": None,
        "target_table": None,
        "risk_market_item": None,
        "problem_type": None,
        "db": None,
        "check_sql": None,
        "note": None,
        "status": None,
    }
    if id == 'null':
        return JsonResponse(data)
    
    sql = f"""select id,check_item,target_table,risk_market_item,problem_type,db,check_sql,note,status
    from check_result_template
    where source_system in ('{company}') and id={id}"""
    conn = db_config.sqlalchemy_conn()
    try:
        result = pd.read_sql(sql, con=conn)
        data = {
            "check_item": result['check_item'].values.tolist()[0],
            "target_table": result['target_table'].values.tolist()[0],
            "risk_market_item": result['risk_market_item'].values.tolist()[0],
            "problem_type": result['problem_type'].values.tolist()[0],
            "db": result['db'].values.tolist()[0],
            "check_sql": result['check_sql'].values.tolist()[0],
            "note": result['note'].values.tolist()[0],
            "status": result['status'].values.tolist()[0],
        }
        return JsonResponse(data)
    except Exception as e:
        return HttpResponseBadRequest(e)
    finally:
        conn.dispose()


@require_http_methods(['POST'])
def rule_update(request):
    """
    执行修改检核规则
    """
    id = request.POST.get('id')
    source_system = request.POST.get('source_system')
    check_item = request.POST.get('check_item')
    target_table = request.POST.get('target_table')
    risk_market = request.POST.get('risk_market')
    problem_type = request.POST.get('problem_type')
    db = request.POST.get('db')
    check_sql = request.POST.get('check_sql')
    note = request.POST.get('note')
    status = request.POST.get('status')

    # 把"转义为'，再把'转义为''
    check_sql = MySQLdb.escape_string(check_sql).decode('utf-8')
    # print(check_sql)
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


@require_http_methods(['POST'])
def rule_add(request):
    """
    新增检核规则
    """
    source_system = request.POST.get('source_system')
    check_item = request.POST.get('check_item')
    target_table = request.POST.get('target_table')
    risk_market = request.POST.get('risk_market')
    problem_type = request.POST.get('problem_type')
    db = request.POST.get('db')
    check_sql = request.POST.get('check_sql')
    note = request.POST.get('note')
    status = request.POST.get('status')

    # 处理检核SQL中含有''的情况
    check_sql = MySQLdb.escape_string(check_sql).decode('utf-8')
    # print(check_sql)
    try:
        # 连接数据库
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        curs.execute('set autocommit=0')
        sql = "select max(id)+1 from check_result_template where source_system in ('" + source_system + "')"
        curs.execute(sql)
        result = curs.fetchone()
        new_id = str(result[0])  # 获取新增的id
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


@require_http_methods(['POST'])
def rule_status_modify(request):
    """修改检核规则状态，禁用/启用 规则的状态
    """
    id = request.POST.get('id')
    post_status = request.POST.get('status')
    company = request.POST.get('company')

    conn = db_config.mysql_connect()
    curs = conn.cursor()
    curs.execute('set autocommit=0')
    # 修改状态
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


@require_http_methods(['POST'])
def rule_execute(request):
    """执行检核
    """
    company = request.POST.get('company')
    username = request.POST.get('username')
    quarter = request.POST.get('quarter')
    source_system = company

    if company == 'xt':
        check = Check()
        if check.init_table(company, source_system, quarter):
            # 初始化3个线程
            thread1 = MyThread(func=check.run_check,
                               args=(company, source_system, quarter, 'oracle'))
            thread2 = MyThread(func=check.run_check,
                               args=(company, source_system, quarter, 'sqlserver'))
            thread3 = MyThread(func=check.xt_spec, args=(quarter,))
            thread4 = MyThread(func=check.run_check,
                               args=(company, source_system, quarter, 'mysql'))
            # 开启3个线程
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

    if run is True:
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


def enable_crontab(request):
    """修改crontab状态
    """
    status = request.POST.get('status')

    cron = CronTab(user=True)
    job = list(cron.find_comment('自动进行数据质量检核'))[0]

    if status == 'false':
        # job.enable(False)
        # cron.write()
        return JsonResponse({"msg": "操作成功"})
    elif status == 'true':
        # job.enable()
        # cron.write()
        return JsonResponse({"msg": "操作成功"})
    else:
        return JsonResponse({"msg": "操作失败"})


def update_crontab(request):
    """更新crontab命令
    """
    job_time = request.POST.get('job_time')

    try:
        # cron  = CronTab(user=True)
        # job = list(cron.find_comment('自动进行数据质量检核'))[0]
        # job.setall(job_time)
        return JsonResponse({"msg": "操作成功"})
    except Exception as e:
        return JsonResponse({"msg": "操作失败", "reason": e})
    
    
@require_http_methods(['GET'])
def query_check_progress(request):
    """
    查询正在运行的检核任务执行进度
    :param request:
    :return:
    """
    company = request.GET.get('company')
    
    try:
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        sql  = f"""select count(*) from check_result_{company} a,(select max(check_version) check_version from check_result_{company}) b
                    where a.check_sql is not null
                    and a.check_sql != ''
                    and a.check_version=b.check_version"""
        curs.execute(sql)
        result = curs.fetchone()
        to_be_check_cnt = result[0]
            
        sql  = f"""select count(*) from check_result_{company} a,(select max(check_version) check_version from check_result_{company}) b
                    where a.check_sql is not null
                    and a.check_sql != ''
                    and a.check_version=b.check_version
                    and a.update_flag='Y'"""
        curs.execute(sql)
        result = curs.fetchone()
        checked_cnt = result[0]
        
        value = round(checked_cnt/to_be_check_cnt*100,2)
        return JsonResponse({"data": value})
    except Exception as e:
        return JsonResponse({"msg": "查询失败", "reason": e})
    finally:
        curs.close()
        conn.close()