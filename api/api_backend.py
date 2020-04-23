from django.http.response import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
import pandas as pd

from mysite import db_config


@require_http_methods(['GET'])
def db_query(request):
    try:
        conn = db_config.sqlalchemy_conn()
        db = pd.read_sql("select name,db_type,db,ip,note,id from source_db_info order by name,db_type", con=conn)
        data = {
            'company': db['name'].values.tolist(),
            'db_type': db['db_type'].values.tolist(),
            'db': db['db'].values.tolist(),
            'ip': db['ip'].values.tolist(),
            'note': db['note'].values.tolist(),
            'rowid': db['id'].values.tolist()
        }
        return JsonResponse({'data': data, 'code': 1000})
    except Exception as e:
        return HttpResponseBadRequest(content=e)
    finally:
        conn.dispose()


@require_http_methods(['POST'])
def db_update(request):
    id = request.POST.get('id')
    ip = request.POST.get('ip')
    user = request.POST.get('user')
    password = request.POST.get('password')
    db = request.POST.get('db')
    port = request.POST.get('port')
    db_type = request.POST.get('db_type')
    note = request.POST.get('note')
    
    try:
        conn = db_config.mysql_connect()
        # with conn.cursor() as curs:
        #     sql = f"""update source_db_info
        #                 set ip='{ip}',
        #                 user='{user}',
        #                 passwd='{password}',
        #                 db='{db}',
        #                 port={port},
        #                 db_type='{db_type}',
        #                 note='{note}'
        #                 where id={id}"""
        #     curs.execute(sql)
        # conn.commit()
        return JsonResponse({'data': '修改成功', 'code': 1000})
    except Exception as e:
        conn.rollback()
        return HttpResponseBadRequest(content=e)
    finally:
        conn.close()

 
@require_http_methods(['POST'])
def db_insert(request):
    company = request.POST.get('company')
    name = request.POST.get('name')
    ip = request.POST.get('ip')
    user = request.POST.get('user')
    password = request.POST.get('password')
    db = request.POST.get('db')
    port = request.POST.get('port')
    db_type = request.POST.get('db_type')
    note = request.POST.get('note')
        
    try:
        conn = db_config.mysql_connect()
        # with conn.cursor() as curs:
        #     sql = f"""insert into source_db_info(company,name,ip,user,passwd,db,port,db_type,note)
        #                 values('{company}','{name}','{ip}','{user}','{password}','{db}',{port},'{db_type}','{note}')"""
        #     curs.execute(sql)
        # conn.commit()
        return JsonResponse({'data': '新增成功', 'code': 1000})
    except Exception as e:
        conn.rollback()
        return HttpResponseBadRequest(content=e)
    finally:
        conn.close()

 
