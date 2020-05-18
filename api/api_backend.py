from django.http.response import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
import pandas as pd

from mysite import db_config


def encrypy_password(connection_string):
    """将连接串中的密码替换为*号
    """
    str1 = connection_string.split('@')[0].split(':')[0]
    str2 = connection_string.split('@')[0].split(':')[1]
    str3 = connection_string.split('@')[1]
    return f'{str1}:{str2}:******@{str3}'


@require_http_methods(['GET'])
def db_query(request):
    try:
        conn = db_config.sqlalchemy_conn()
        db = pd.read_sql("select name,db_type,alias,connection_string,db,ip,note,id from source_db_info order by name,db_type", con=conn)
        
        db['connection_string'] = db['connection_string'].apply(encrypy_password)
        
        data = {
            'company': db['name'].values.tolist(),
            'db_type': db['db_type'].values.tolist(),
            'alias': db['alias'].values.tolist(),
            'connection_string': db['connection_string'].values.tolist(),
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
    alias = request.POST.get('alias')
    user = request.POST.get('user')
    password = request.POST.get('password')
    db = request.POST.get('db')
    port = request.POST.get('port')
    db_type = request.POST.get('db_type')
    charset = request.POST.get('charset')
    note = request.POST.get('note')
    
    if db_type == 'mysql':
        connection_string = f'mysql+mysqldb://{user}:{password}@{ip}:{port}/{db}?charset={charset}'
    elif db_type == 'oracle':
        connection_string = f'oracle://{user}:{password}@{ip}:{port}/?service_name={db}'
    elif db_type == 'sqlserver':
        connection_string = f'mssql+pymssql://{user}:{password}@{ip}:{port}/{db}?charset={charset}'
    elif db_type == 'postgresql':
        connection_string = f'postgresql://{user}:{password}@{ip}:{port}/{db}'
    
    try:
        # conn = db_config.mysql_connect()
        # with conn.cursor() as curs:
        #     sql = f"""update source_db_info
        #                 set alias='{alias}',
        #                 connection_string='{connection_string}',
        #                 ip='{ip}',
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
    alias = request.POST.get('alias')
    ip = request.POST.get('ip')
    user = request.POST.get('user')
    password = request.POST.get('password')
    db = request.POST.get('db')
    port = request.POST.get('port')
    db_type = request.POST.get('db_type')
    charset = request.POST.get('charset')
    note = request.POST.get('note')
    
    if db_type == 'mysql':
        connection_string = f'mysql+mysqldb://{user}:{password}@{ip}:{port}/{db}?charset={charset}'
    elif db_type == 'oracle':
        connection_string = f'oracle://{user}:{password}@{ip}:{port}/?service_name={db}'
    elif db_type == 'sqlserver':
        connection_string = f'mssql+pymssql://{user}:{password}@{ip}:{port}/{db}?charset={charset}'
    elif db_type == 'postgresql':
        connection_string = f'postgresql://{user}:{password}@{ip}:{port}/{db}'
        
    try:
        conn = db_config.mysql_connect()
        # with conn.cursor() as curs:
        #     sql = f"""insert into source_db_info(company,name,alias,connection_string,ip,user,passwd,db,port,db_type,note)
        #                 values('{company}','{name}','{alias}','{connection_string}','{ip}','{user}','{password}','{db}',{port},'{db_type}','{note}')"""
        #     curs.execute(sql)
        # conn.commit()
        return JsonResponse({'data': '新增成功', 'code': 1000})
    except Exception as e:
        conn.rollback()
        return HttpResponseBadRequest(content=e)
    finally:
        conn.close()

 
