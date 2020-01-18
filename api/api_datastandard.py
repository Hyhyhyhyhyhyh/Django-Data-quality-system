from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

import sys, MySQLdb
sys.path.insert(0, '..')
from mysite import db_config


def db_query(std_name, std_type):
    conn = db_config.mysql_connect()
    curs = conn.cursor()
    if std_type == 'detail':
        '''
        请求类型：GET

        请求参数：std_name数据标准名

        返回参数：
            id                      主键id
            std_id                  标准编号
            name                    标准名称
            en_name                 标准英文名称
            business_definition     业务定义
            business_rule           业务规则
            std_source              标准来源
            data_type               数据类型
            data_format             数据格式
            code_rule               编码规则
            code_range              编码范围
            code_meaning            编码含义
            business_range          业务范围
            dept                    数据责任部门
            system                  数据使用系统
        '''
        sql = f"select id,std_id,name,en_name,business_definition,business_rule,std_source,data_type,data_format,code_rule,code_range,code_meaning,business_range,dept,system from data_standard_detail where name='{std_name}'"
        curs.execute(sql)
        result = curs.fetchone()
        return {
            'name': result[2],
            'en_name': result[3],
            'business_definition': result[4],
            'business_rule': result[5],
            'std_source': result[6],
            'data_type': result[7],
            'data_format': result[8],
            'code_rule': result[9],
            'code_range': result[10],
            'code_meaning': result[11],
            'business_range': result[12],
            'dept': result[13],
            'system': result[14],
        }
    elif std_type == 'desc':
        '''
        请求类型：GET

        请求参数：std_name数据标准名

        返回参数：
            id          主键id
            name        标准名称
            content     标准内容    
        '''
        sql = f"select id,name,content from data_standard_desc where name='{std_name}'"
        curs.execute(sql)
        result = curs.fetchone()
        return {
            'name': result[1],
            'content': result[2],
        }
    curs.close()
    conn.close()


# 查询数据标准
@require_http_methods(["GET"])
def query_detail(request):
    std_name = request.GET.get('std_name')
    std_type = request.GET.get('std_type')

    if all([std_name, std_type]) == False:
        return JsonResponse({'msg':'请求参数缺失', 'code': 3000})

    data = db_query(std_name, std_type)
    return JsonResponse(data)
    

# 查询数据标准编辑记录
@require_http_methods(["GET"])
def query_update_history(request):
    std_name = request.GET.get('std_name')

    if std_name is None:
        return JsonResponse({'msg':'请求参数缺失', 'code': 3000})
        
    conn = db_config.mysql_connect()
    curs = conn.cursor()
    sql  = f"select username,update_time from data_standard_update_log where std_name='{std_name}' order by update_time desc limit 1"
    if curs.execute(sql) == 1:
        result = curs.fetchone()
        return JsonResponse({'username': result[0], 'last_update_time': str(result[1])})
    else:
        return JsonResponse({'username': None, 'last_update_time': None})
    
# 更新数据标准
@require_http_methods(["POST"])
def update(request):
    username            = request.POST.get('username')
    std_type            = request.POST.get('std_type')
    std_name            = request.POST.get('std_name')
    en_name             = request.POST.get('en_name')
    business_definition = request.POST.get('business_definition')
    business_rule       = request.POST.get('business_rule')
    std_source          = request.POST.get('std_source')
    data_type           = request.POST.get('data_type')
    data_format         = request.POST.get('data_format')
    code_rule           = request.POST.get('code_rule')
    code_range          = request.POST.get('code_range')
    code_meaning        = request.POST.get('code_meaning')
    business_range      = request.POST.get('business_range')
    dept                = request.POST.get('dept')
    system              = request.POST.get('system')
    content             = request.POST.get('content')

    conn = db_config.mysql_connect()
    curs = conn.cursor()
    curs.execute('set autocommit=0')

    if all([std_name, std_type]) == False:
        return JsonResponse({'msg':'请求参数缺失', 'code': 3000})
    
    # post内容与数据库内容对比，如果内容一致则无需update
    orgin_data = db_query(std_name, std_type)

    if std_type == 'desc':
        post_data = {'name': std_name, 'content': content}

        if post_data == orgin_data:
            return JsonResponse({'msg':'内容一致，无需修改', 'code': 1001})
        else:
            try:
                # 把上一版本的数据标准内容存入到日志表
                update_log = str(orgin_data.items() - post_data.items())    # 将被update替换的内容
                sql = f"insert into data_standard_update_log(std_name, username, previous_version) values('{std_name}', '{username}', \"{update_log}\")"
                curs.execute(sql)
                conn.commit()

                # 更新数据标准
                sql = f"update data_standard_desc set name='{std_name}', content='{content}' where name='{std_name}'"
                curs.execute(sql)
                conn.commit()
                curs.close()
                conn.close()
                return JsonResponse({'msg':'修改成功', 'code': 1000})
            except Exception as e:
                return JsonResponse({'msg':e, 'code': 2000})
    elif std_type == 'detail':
        post_data = {
            'name'               : std_name,
            'en_name'            : en_name,
            'business_definition': business_definition,
            'business_rule'      : business_rule,
            'std_source'         : std_source,
            'data_type'          : data_type,
            'data_format'        : data_format,
            'code_rule'          : code_rule,
            'code_range'         : code_range,
            'code_meaning'       : code_meaning,
            'business_range'     : business_range,
            'dept'               : dept,
            'system'             : system,
        }

        if post_data == db_query(std_name, std_type):
            return JsonResponse({'msg':'内容一致，无需修改', 'code': 1001})
        else:
            try:
                # 把上一版本的数据标准内容存入到日志表
                update_log = str(orgin_data.items() - post_data.items())    # 将被update替换的内容
                sql = f"insert into data_standard_update_log(std_name, username, previous_version) values('{std_name}', '{username}', \"{update_log}\")"
                curs.execute(sql)
                conn.commit()

                sql = f"""update data_standard_detail set name = '{std_name}', 
                                                    en_name = '{en_name}',
                                                    business_definition = '{business_definition}', 
                                                    business_rule = '{business_rule}',
                                                    std_source = '{std_source}',
                                                    data_type = '{data_type}',
                                                    data_format = '{data_format}',
                                                    code_rule = '{code_rule}',
                                                    code_range = '{code_range}',
                                                    code_meaning = '{code_meaning}',
                                                    business_range = '{business_range}',
                                                    dept = '{dept}',
                                                    system = '{system}'
                    where name='{std_name}'"""
                curs.execute(sql)
                conn.commit()
                curs.close()
                conn.close()
                return JsonResponse({'msg': '修改成功', 'code': 1000})
            except Exception as e:
                return JsonResponse({'msg': str(e), 'code': 2000})


# 获取数据标准目录
@require_http_methods(["GET"])
def query_index(request):
    conn = db_config.mysql_connect()
    curs = conn.cursor()

    sql = "select idx_id, idx_pid,idx_name,is_open from data_standard_index"
    curs.execute(sql)
    result = curs.fetchall()

    data = []
    for i in result:
        data.append({
            'id':   i[0],
            'pId':  i[1],
            'name': i[2],
            't':    i[2],
            'open': i[3]
        })

    curs.close()
    conn.close()
    return JsonResponse(data, safe=False)