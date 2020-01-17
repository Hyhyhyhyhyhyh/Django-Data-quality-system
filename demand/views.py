from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.http.response import JsonResponse
from django import forms
#import django_excel as excel

# 引入自定义函数
import sys, MySQLdb, json
sys.path.insert(0, '..')
from utils import query  #获取所有季度名
from mysite import db_config  #连接数据库
from utils.functions import is_login


def list_subcompany(request):
    company = request.GET.get('company')
    if company == 'xt':
        company = '信托'
    elif company == 'zc':
        company = '资产'
    elif company == 'db':
        company = '担保'
    elif company == 'jk':
        company = '金科'
    elif company == 'fd2':
        company = '基金2'
    elif company == 'fd1':
        company = '基金1'
    elif company == 'jz':
        company = '金租'
    conn = db_config.mysql_connect()
    curs = conn.cursor()
    sql = "select rownum,company,item_name,demand_name,demand_created,group_concat(quarter,status order by quarter asc separator'|') \
            from source_system_demand \
            where id in ( select max(id) from source_system_demand where company='{0}' group by company,item_name,quarter ) \
            group by rownum,company;".format(company)
    curs.execute(sql)
    result = curs.fetchall()
    result_list = []
    for i in result:
        result_list_tmp = []
        result_list_tmp.append(i[0])
        result_list_tmp.append(i[1])
        result_list_tmp.append(i[2])
        result_list_tmp.append(i[3])
        result_list_tmp.append(i[4])
        for t in i[5].split('|'):
            result_list_tmp.append(t)
        result_list.append(result_list_tmp)
    curs.close()
    conn.close()
    return JsonResponse(result_list, safe=False)


@is_login
def query(request):
    username = request.session['username']
    conn = db_config.mysql_connect()
    curs = conn.cursor()
    sql = "select rownum,company,item_name,demand_name,demand_created,quarter,status from source_system_demand where id in ( select max(id) from source_system_demand group by company,item_name,quarter ) order by company,rownum asc"
    return render(request, "demand/query.html", {
        "username": username,
    })


class UploadFileForm(forms.Form):
    file = forms.FileField()


def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_data = request.FILES['file'].get_array()
            excel_data = json.dumps(excel_data)
            with open('static/resource/demand.json', 'w') as file:
                file.write(excel_data)
            return HttpResponse("Excel处理成功，请返回首页查看数据")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(request, 'demand/upload_form.html', {'form': form})
