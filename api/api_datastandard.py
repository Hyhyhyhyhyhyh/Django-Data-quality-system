from django.http.response import JsonResponse

import sys,MySQLdb
sys.path.insert(0, '..')
from mysite import db_config

# 查询数据标准
def query(request):
    std_name = request.GET.get('std_name')
    std_type = request.GET.get('std_type')

    conn = db_config.mysql_connect()
    curs = conn.cursor()

    if all([std_name, std_type]) == False:
        return JsonResponse({'msg':'请求参数名缺失'})
    
    if std_type == 'detail':
        data = {
            "id": 1,
            "std_id": "PC000001",
            "name": "项目编号",
            "en_name": "Project Number",
            "business_definition": "业务定义",
            "business_rule": "业务规则",
            "std_source": "/",
            "data_type": "文本",
            "data_format": "Varchar (250)",
            "code_rule": "/",
            "code_range": "/",
            "code_meaning": "/",
            "business_range": "业务范围",
            "dept": "xx部门",
            "system": "/"
        }
        return JsonResponse(data)
    elif std_type == 'desc':
        data = {
            "id": 1,
            "name": "概述",
            "content": "概述"
        }
        return JsonResponse(data)

    
    
# 更新数据标准
def update(request):
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

    if all([std_name, std_type]) == False:
        return JsonResponse({'msg':'请求参数名缺失'})
    
    if std_type == 'desc':
        try:
            return JsonResponse({'msg':'修改成功', 'code': 1000})
        except Exception as e:
            return JsonResponse({'msg':e, 'code': 2000})
    elif std_type == 'detail':
        try:
            return JsonResponse({'msg': '修改成功', 'code': 1000})
        except Exception as e:
            return JsonResponse({'msg': str(e), 'code': 2000})