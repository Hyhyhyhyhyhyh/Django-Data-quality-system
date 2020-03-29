from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

import sys

sys.path.insert(0, '..')
from mysite import db_config


@require_http_methods(['GET'])
def quality_detail(request):
    """
    查询给定日期的检核明细结果，返回最新版本数据
    """
    company = request.GET.get('company')
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    month = request.GET.get('month')
    day = request.GET.get('day')
    
    try:
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        sql  = f"""select id,
				source_system,
				check_item,
				target_table,
				risk_market_item,
				problem_type,
				check_sql,
				item_count,
				problem_count,
				concat(problem_per,'%'),
				note,
				check_date
				from check_result_{company} a,
				(
					select max(a.check_version) check_version
					from check_result_{company} a,dim_date b where DATE_FORMAT(a.check_date,'%Y%m%d') = b.day_id
					and b.year={year}
					and b.quarter={quarter}
					and b.month={month}
					and b.day={day}
				) b
				where a.risk_market_item='是'
				and a.check_version=b.check_version
				order by id asc"""
        curs.execute(sql)
        result = curs.fetchall()
        
        result_list = []
        for i in result:
            result_dict = {"id": i[0], "source_system": i[1], "check_item": i[2], "target_table": i[3], "risk_market_item": i[4],
                           "problem_type": i[5], "check_sql": i[6], "item_count": i[7], "problem_count": i[8], "problem_per": i[9],
                           "note": i[10], "check_date": i[10]}
            result_list.append(result_dict)
        return JsonResponse({'data': result_list})
    except Exception as e:
        print(e)
        return JsonResponse({'msg': str(e)})
    finally:
        curs.close()
        conn.close()
        
        
@require_http_methods(['GET'])
def report_detail(request):
    """
    查询给定日期，各公司的检核明细结果，返回最新版本数据
    """
    company = request.GET.get('company')
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    month = request.GET.get('month')
    day = request.GET.get('day')
    
    try:
        conn = db_config.mysql_connect()
        curs = conn.cursor()
        sql  = f"""select a.check_item,a.problem_type,a.problem_count,a.item_count,concat(a.problem_per,'%') problem_per 
                    from check_result_{company} a,
                    (
                        select max(a.check_version) check_version
                        from check_result_{company} a,dim_date b where DATE_FORMAT(a.check_date,'%Y%m%d') = b.day_id
                        and b.year={year}
                        and b.quarter={quarter}
                        and b.month={month}
                        and b.day={day}
                    ) b
                    where a.risk_market_item='是'
                    and a.check_version=b.check_version
                    and (a.problem_count<>0 or a.problem_count is null)
                    order by a.problem_type,a.problem_count desc"""
        curs.execute(sql)
        result = curs.fetchall()
        
        result_list = []
        for i in result:
            result_dict = {"check_item": i[0],
                           "problem_type": i[1],
                           "problem_count": i[2],
                           "item_count": i[3],
                           "problem_per": i[4],
                           }
            result_list.append(result_dict)
        return JsonResponse({'data': result_list})
    except Exception as e:
        print(e)
        return JsonResponse({'msg': str(e)})
    finally:
        curs.close()
        conn.close()