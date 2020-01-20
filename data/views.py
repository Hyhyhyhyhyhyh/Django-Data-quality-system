import sys

from django.shortcuts import render

sys.path.insert(0, '..')
from utils import report_data  # 引用report_data.py获取数据质量报告的各项数据
from utils.functions import is_login
from utils import functions as f


@is_login
def dashboard(request):
    """集团仪表盘
    说明：本模块分3部分在前端展示
    1. 第一行为3个数据概览统计
    2. 第二行统计各个公司数据质量问题概况
    3. 第三行使用pyecharts做的数据统计图
    """
    username = request.session['username']
    quarter = f.get_user_quarter(request)
    db_quarter_list = f.get_quarter_list()  # 获取检核结果库中所有季度的列表

    return render(
        request, "data/dashboard.html", {
            "quarter": quarter,
            "db_quarter_list": db_quarter_list,
            "username": username,
        })


@is_login
def dashboard_subcompany(request):
    """子公司仪表盘
    说明：本模块分3部分在前端展示
    1. 子公司问题数据项的分布
    2. 子公司问题数据项的排序报表
    3. 改造进度
    """
    username = request.session['username']
    company = request.GET.get('name')
    company_zh = request.GET.get('company')
    quarter = f.get_user_quarter(request)
    db_quarter_list = f.get_quarter_list()  # 获取检核结果库中所有季度的列表

    # 获取仪表盘数据
    return render(
        request, "data/dashboard_subcompany.html", {
            "company": company,
            "company_zh": company_zh,
            "quarter": quarter,
            "db_quarter_list": db_quarter_list,
            "username": username,
        })


@is_login
def result_detail(request):
    """检核结果Excel明细
    """
    quarter = f.get_user_quarter(request)
    company = request.GET.get('name')
    username = request.session['username']
    result = f.get_result_detail(company, quarter)  # 获取检核结果Excel明细
    db_quarter_list = f.get_quarter_list()  # 获取检核结果库中所有季度的列表

    return render(
        request, "data/result_detail.html", {
            "quarter": quarter,
            "username": username,
            "result_tab": result,
            "db_quarter_list": db_quarter_list,
            "company": company
        })


@is_login
def report(request):
    """检核报告Word
    """
    username = request.session['username']
    quarter = f.get_user_quarter(request)
    db_quarter_list = f.get_quarter_list()  # 获取检核结果库中所有季度的列表

    # 引用report_data.py获取数据质量报告的各项数据
    sum_item_cnt = report_data.risk_market_total_count(quarter)
    sum_problem_cnt = report_data.risk_market_problem_count(quarter)
    total_problem_per = str(round(sum_problem_cnt / sum_item_cnt * 100, 2)) + "%"
    detail = []
    for company in ('xt', 'zc', 'db', 'jk', 'jj1', 'jj2', 'jz'):
        detail.append(report_data.risk_market_problem_detail(company, quarter))

    return render(
        request, "data/report.html", {
            "quarter": quarter,
            "username": username,
            "db_quarter_list": db_quarter_list,
            "sum_item_cnt": sum_item_cnt,
            "sum_problem_cnt": sum_problem_cnt,
            "total_problem_per": total_problem_per,
            "xt_detail": detail[0],
            "zc_detail": detail[1],
            "db_detail": detail[2],
            "jk_detail": detail[3],
            "jj1_detail": detail[4],
            "jj2_detail": detail[5],
            "jz_detail": detail[6]
        })
