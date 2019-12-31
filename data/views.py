from django.shortcuts import render,redirect

import sys, os, math, datetime
sys.path.insert(0, '..')
from utils import report_data          #引用report_data.py获取数据质量报告的各项数据
from utils import query                #引用query.py简便查询各种数据库信息


#-------------------------------------------------------- 仪表盘 --------------------------------------------------------#
# 说明：本模块分3部分在前端展示
## 1. 第一行为3个数据概览统计
## 2. 第二行统计各个公司数据质量问题概况
## 3. 第三行使用pyecharts做的数据统计图

def dashboard(request):
    if request.session.get('is_login',None) is None:    #从session信息中判断登录状态，为None则跳转至登录页
        return redirect("../../authorize/login")
    
    username = request.session['username']
    if request.GET.get('quarter') is None:  #url没有传参的话，仪表盘显示上一季度数据
        if request.session.get('selected_quarter',None) is None:
            quarter = str(datetime.datetime.now().year)+"Q"+str(math.ceil(datetime.datetime.now().month/3.)-1)
        else:
            quarter = request.session['selected_quarter']
    else:
        quarter = request.GET.get('quarter')
        request.session['selected_quarter'] = request.GET.get('quarter')
    db_quarter_list = query.get_quarter_list()   #获取检核结果库中所有季度的列表
    return render(request,"data/dashboard.html",{"quarter": quarter,
                                                 "db_quarter_list": db_quarter_list,
                                                 "username": username,
                })

#-------------------------------------------------------- 子公司仪表盘 --------------------------------------------------------#
# 说明：本模块分3部分在前端展示
## 1. 子公司问题数据项的分布
## 2. 子公司问题数据项的排序报表
## 3. 改造进度

def dashboard_subcompany(request):
    if request.session.get('is_login',None) is None:
        return redirect("../../authorize/login")

    username = request.session['username']
    if request.GET.get('quarter') is None:  #url没有传参的话，仪表盘显示上一季度数据
        if request.session.get('selected_quarter',None) is None:
            quarter = str(datetime.datetime.now().year)+"Q"+str(math.ceil(datetime.datetime.now().month/3.)-1)
        else:
            quarter = request.session['selected_quarter']
    else:
        quarter = request.GET.get('quarter')
        request.session['selected_quarter'] = request.GET.get('quarter')

    company    = request.GET.get('name')
    company_zh = request.GET.get('company_zh')

    db_quarter_list = query.get_quarter_list()   #获取检核结果库中所有季度的列表
    #获取仪表盘数据
    return render(request,"data/dashboard_subcompany.html",{"company":company,
                                                            "company_zh": company_zh,
                                                            "quarter":quarter,
                                                            "db_quarter_list": db_quarter_list,
                                                            "username": username,
                                                            })

#-------------------------------------------------------- 检核结果Excel明细 --------------------------------------------------------#
def result_detail(request):
    if request.session.get('is_login',None) is None:
        return redirect("../../authorize/login")
    
    if request.GET.get('quarter') is None:  #url没有传参的话，仪表盘显示上一季度数据
        if request.session.get('selected_quarter',None) is None:
            quarter = str(datetime.datetime.now().year)+"Q"+str(math.ceil(datetime.datetime.now().month/3.)-1)
        else:
            quarter = request.session['selected_quarter']
    else:
        quarter = request.GET.get('quarter')
        request.session['selected_quarter'] = request.GET.get('quarter')

    company = request.GET.get('name')
    username = request.session['username']

    result = query.get_result_detail(company, quarter)  #获取检核结果Excel明细
    db_quarter_list = query.get_quarter_list()         #获取检核结果库中所有季度的列表

    return render(request,"data/result_detail.html",{"quarter": quarter,
                                                        "username": username,
                                                        "result_tab": result,
                                                        "db_quarter_list": db_quarter_list,
                                                        "company": company
                                                    }
                )
    
#-------------------------------------------------------- 检核报告Word --------------------------------------------------------#
def report(request):
    if request.session.get('is_login',None) is None:
        return redirect("../../authorize/login")

    if request.GET.get('quarter') is None:  #url没有传参的话，仪表盘显示上一季度数据
        if request.session.get('selected_quarter',None) is None:
            quarter = str(datetime.datetime.now().year)+"Q"+str(math.ceil(datetime.datetime.now().month/3.)-1)
        else:
            quarter = request.session['selected_quarter']
    else:
        quarter = request.GET.get('quarter')
        request.session['selected_quarter'] = request.GET.get('quarter')

    username = request.session['username']
    db_quarter_list = query.get_quarter_list()     #获取检核结果库中所有季度的列表

    #引用report_data.py获取数据质量报告的各项数据
    sum_item_cnt      = report_data.risk_market_total_count(quarter)
    sum_problem_cnt   = report_data.risk_market_problem_count(quarter)
    total_problem_per = str(round(sum_problem_cnt/sum_item_cnt*100,2))+"%"
    xt_detail         = report_data.risk_market_problem_detail("xt",quarter)
    zc_detail         = report_data.risk_market_problem_detail("zc",quarter)
    db_detail         = report_data.risk_market_problem_detail("db",quarter)
    jk_detail         = report_data.risk_market_problem_detail("jk",quarter)
    jj1_detail        = report_data.risk_market_problem_detail("jj1",quarter)
    jj2_detail        = report_data.risk_market_problem_detail("jj2",quarter)
    jz_detail         = report_data.risk_market_problem_detail("jz",quarter)
    return render(request,"data/report.html",{"quarter": quarter,
                                                "username": username,
                                                "db_quarter_list": db_quarter_list,
                                                "sum_item_cnt": sum_item_cnt,
                                                "sum_problem_cnt": sum_problem_cnt,
                                                "total_problem_per": total_problem_per,
                                                "xt_detail":xt_detail,
                                                "zc_detail":zc_detail,
                                                "db_detail":db_detail,
                                                "jk_detail":jk_detail,
                                                "jj1_detail":jj1_detail,
                                                "jj2_detail":jj2_detail,
                                                "jz_detail":jz_detail
                                                }
                )