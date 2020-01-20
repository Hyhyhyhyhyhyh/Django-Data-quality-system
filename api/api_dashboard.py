import sys

import numpy as np
from django.http.response import JsonResponse

# np.set_printoptions(precision=2, suppress=True)
sys.path.insert(0, '..')


def avg_problem_percentage(request):
    """各公司平均问题占比
    """
    data = [
        ["quarter", "2019Q1", "2019Q2", "2019Q3", "2019Q4"],
        ["信托",  round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2)],
        ["资产",  round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2)],
        ["担保",  round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2)],
        ["金科",  round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2)],
        ["基金1", round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2)],
        ["基金2", round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2)],
        ["金租",  round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2), round(np.random.rand(), 2)],
    ]
    return JsonResponse(data, safe=False)


def same_problem_top5(request):
    """各公司同类问题Top 5统计
    """
    quarter = request.GET.get('quarter')

    if quarter == '2019Q1':
        name = ["交易本金金额", "机构证件号码", "机构证件类别", "项目名称", "其他"]
        value = [round(i,2) for i in np.random.rand(5).tolist()]
    elif quarter == '2019Q2':
        name = ["项目金额", "参与人角色标识", "项目余额", "机构证件类别", "其他"]
        value = [round(i,2) for i in np.random.rand(5).tolist()]
    elif quarter == '2019Q3':
        name = ["交易本金金额", "机构证件号码", "机构证件类别", "项目名称", "其他"]
        value = [round(i,2) for i in np.random.rand(5).tolist()]
    elif quarter == '2019Q4':
        name = ["项目金额", "参与人角色标识", "项目余额", "机构证件类别", "其他"]
        value = [round(i,2) for i in np.random.rand(5).tolist()]
    return JsonResponse({'name': name, 'value': value})


def subcompany_data_percentage(request):
    """各公司数据量占比
    """
    quarter = request.GET.get('quarter')

    data = [
        {
            "name": "信托",
            "value": np.random.randint(1000,99999)
        },
        {
            "name": "资产",
            "value": np.random.randint(1000,99999)
        },
        {
            "name": "担保",
            "value": np.random.randint(1000,99999)
        },
        {
            "name": "金科",
            "value": np.random.randint(1000,99999)
        },
        {
            "name": "基金1",
            "value": np.random.randint(1000,99999)
        },
        {
            "name": "基金2",
            "value": np.random.randint(1000,99999)
        },
        {
            "name": "金租",
            "value": np.random.randint(1000,99999)
        }]
    return JsonResponse(data, safe=False)


def count_db_rows(request):
    """统计各类数据库数据量
    """
    quarter = request.GET.get('quarter')
    
    data = [{
                "name": "MySQL",
                "value": np.random.randint(1000,99999),
            },
            {
                "name": "Oracle",
                "value": np.random.randint(1000,99999)
            },
            {
                "name": "SQL server",
                "value": np.random.randint(1000,99999)
            },
            {
                "name": "HBase",
                "value": np.random.randint(1000,99999)
            },
            ]
    return JsonResponse(data, safe=False)


def data_overiew(request):
    """统计风险集市相关 总数据量、总问题数据量、总问题占比
    """
    quarter = request.GET.get('quarter')
    
    all_cnt     = np.random.randint(555550,999999)
    problem_cnt = all_cnt - 555550
    data = {
        "all_cnt": all_cnt,
        "problem_cnt": problem_cnt,
        "problem_per": round(problem_cnt / all_cnt * 100, 2)
        }
    return JsonResponse(data)
    
    
def total_trend(request):
    """显示集团总问题占比走势
    """
    data = {"quarter": ["2019Q1", "2019Q2", "2019Q3", "2019Q4"], "value": [round(i,2) for i in np.random.rand(4).tolist()]}
    return JsonResponse(data)

# 子公司仪表盘-问题项统计
def subcompany_problem_count(request):
    company = request.GET.get('company')
    quarter = request.GET.get('quarter')
   
    data = [
        ["问题占比", "问题数据总量", "问题数据项"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "风险等级"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "风险资本类别"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "净资本类别"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "参与人角色"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "参与人规模"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "所有制类型"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "参与人角色标识"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "产品收益率"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "参与人上市标识"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "资金或资产来源"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "项目投向行业"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "项目名称"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "项目来源"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "存续标识"],
        [round(np.random.rand()*100, 2), np.random.randint(1000,99999), "产品结束日期"]
    ]
    return JsonResponse(data, safe=False)
