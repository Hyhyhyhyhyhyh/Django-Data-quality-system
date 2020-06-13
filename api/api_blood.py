import re
import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

sys.path.insert(0, '..')
from mysite import db_config


'''
def extract_table_name_from_sql(sql_str):
    """
    提取sql语句中的表名
    """
    # 过滤去除/* */注释
    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql_str)

    # 去除以 -- 或 # 开头的注释行
    lines = [line for line in q.splitlines() if not re.match("^\s*(--|#)", line)]

    # 去除行尾的以 -- 或 # 开头的注释
    q = " ".join([re.split("--|#", line)[0] for line in lines])

    # 根据空格、();分割单词
    tokens = re.split(r"[\s)(;]+", q)

    # 如果发现 from 或 join ，则把get_next设为True，然后获取表名
    result = set()
    get_next = False
    for token in tokens:
        if get_next:
            if token.lower() not in ["", "select"]:
                # result.append(token)
                result.add(token)
            get_next = False
        get_next = token.lower() in ["from", "join"]

    return result
'''
    
@require_http_methods(['GET'])
def query_mapping(request):
    table_name = request.GET.get('table_name')
    
    sql = f"""select distinct subject_area,
                mapping_name,
                source,
				target,
                case when locate('_ts_', mapping_name)>0 then 1
                     when locate('_ti_', mapping_name)>0 then 2
                     when locate('_ods_', mapping_name)>0 then 3
                     else 99
                end level
                from datacenter_mapping
                where (
                    lower(source) like '%{table_name.lower()}%'
                    or lower(target) like '%{table_name.lower()}%'
                    or lower(mapping_name) like '%{table_name.lower()}%'
                    )
                and source<>target
                order by level asc,1,2,3
            """
    
    try:
        conn = db_config.mysql_connect()
        with conn.cursor() as curs:
            curs.execute(sql)
            r = curs.fetchall()
        return JsonResponse({
            'subject_area': [i[0] for i in r],
            'mapping_name': [i[1] for i in r],
            'source': [i[2] for i in r],
            'target': [i[3] for i in r],
            'level': [i[4] for i in r]
        })
    except Exception as e:
        return HttpResponseBadRequest(e)
    finally:
        conn.close()

