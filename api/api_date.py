from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

import datetime
import math

import sys
sys.path.insert(0, '..')
from mysite import db_config
from utils import functions as f

@require_http_methods(['GET'])
def year_list(request):
    '''查询已有检核结果的年份
    '''
    year = f.query_data_year()
    
    if year:
        return JsonResponse({'data': year})
    else:
        return HttpResponse({'获取年份错误'}, status=500)


@require_http_methods(['GET'])
def quarter_list(request):
    '''查询已有检核结果的季度
    '''
    year = request.GET.get('year')
    if not year:
        year = datetime.datetime.now().year

    quarter = f.query_data_quarter(year)
    if quarter:
        return JsonResponse({'data': quarter})
    else:
        return HttpResponse({'获取季度错误'}, status=500)
    

@require_http_methods(['GET'])
def month_list(request):
    '''查询已有检核结果的月份
    '''
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    if not all((year, quarter)):
        year = year or datetime.datetime.now().year
        quarter = quarter or math.ceil(datetime.datetime.now().month/3.)

    month = f.query_data_month(year, quarter)
    if month:
        return JsonResponse({'data': month})
    else:
        return HttpResponse({'获取月份错误'}, status=500)


@require_http_methods(['GET'])
def day_list(request):
    '''查询已有检核结果的天
    '''
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    month = request.GET.get('month')
    if not all((year, quarter, month)):
        year = year or datetime.datetime.now().year
        quarter = quarter or math.ceil(datetime.datetime.now().month/3.)
        month = month or datetime.datetime.now().month

    day = f.query_data_day(year, quarter, month)
    if day:
        return JsonResponse({'data': day})
    else:
        return HttpResponse({'获取天错误'}, status=500)