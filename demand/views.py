import json
import sys

from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.http.response import JsonResponse
from django.shortcuts import render

# import django_excel as excel
sys.path.insert(0, '..')
from mysite import db_config


def list_subcompany(request):
    company = request.GET.get('company')
    conn = db_config.mysql_connect()
    curs = conn.cursor()

    try:
        sql = f"""select rownum,
                        company,
                        item_name,
                        demand_name,
                        demand_created,
                        group_concat(quarter,status order by quarter asc separator'|')
                    from source_system_demand
                    where id in ( select max(id) from source_system_demand where company='{company}' group by company,item_name,quarter )
                    group by rownum,company"""
        curs.execute(sql)
        result = curs.fetchall()

        result_list = []
        for i in result:
            result_list_tmp = [i[0], i[1], i[2], i[3], i[4]]
            for t in i[5].split('|'):
                result_list_tmp.append(t)
            result_list.append(result_list_tmp)
        return JsonResponse(result_list, safe=False)
    except:
        return HttpResponse('error', status=500)
    finally:
        curs.close()
        conn.close()


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
