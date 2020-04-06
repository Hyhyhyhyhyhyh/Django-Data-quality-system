from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
import re
import pandas as pd

import sys
sys.path.insert(0, '..')
from mysite import db_config

def extract_table_name_from_sql(sql_str):
    """
    提取sql语句中的表名
    """
    # 过滤去除/* */注释
    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql_str)

    # 去除以 -- 或 # 开头的注释行
    lines = [line for line in q.splitlines() if not re.match("^\s*(--|#)", line)]

    # 去除行尾的以 -- 或 # 开头的注释
    q = " ".join([re.split("--|#", line)[0] for line in lines])

    # 根据空格、();分割单词
    tokens = re.split(r"[\s)(;]+", q)

    # 如果发现 from 或 join ，则把get_next设为True，然后获取表名
    result = set()
    get_next = False
    for token in tokens:
        if get_next:
            if token.lower() not in ["", "select"]:
                # result.append(token)
                result.add(token)
            get_next = False
        get_next = token.lower() in ["from", "join"]

    return result


@require_http_methods(['GET'])
def blood_analyze(request):
    company = request.GET.get('company')
    
    try:
        engine = db_config.sqlalchemy_conn()
        sql = """select source_system,check_item,target_table,check_sql
                from check_result_template
                where check_sql is not null or check_sql !=''"""
        r = pd.read_sql(sql=sql, con=engine)

        # 提取SQL中的表名
        r['table_name'] = r['check_sql'].apply(extract_table_name_from_sql)
        r.drop('check_sql', inplace=True, axis=1)

        df = pd.DataFrame(columns=['source_system', 'check_item', 'target_table', 'table_name'])

        for i in r.index:
            tables = r.loc[i, 'table_name']
            for t in tables:
                df = df.append(pd.DataFrame({
                    'source_system': r.loc[i, 'source_system'],
                    'check_item': r.loc[i, 'check_item'],
                    'target_table': r.loc[i, 'target_table'],
                    'table_name': t,
                }, index=[0]))
        
        # 去重
        df.drop_duplicates(inplace=True)
                
        # 指标分类
        def classify(t):
            if t is None:
                return '其他'
            if t.find('项目') != -1:
                return '项目类'
            elif t.find('交易') != -1:
                return '交易类'
            elif t.find('机构') != -1:
                return '机构类'
            elif t.find('参与人') != -1:
                return '参与人类'
            elif t.find('产品') != -1:
                return '产品类'
            elif t.find('资产') != -1:
                return '资产类'
            elif t.find('资金') != -1:
                return '资金'
            else:
                return '其他'
            
        df['type'] = df['target_table'].apply(classify)

        df.drop('target_table', inplace=True, axis=1)

        # 排序，重置索引
        df.sort_values(by=['source_system', 'type', 'check_item', 'table_name'], axis=0, ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # 根据公司过滤数据
        df2 = df[df['source_system']==company]
        tree = []
        for name_lv2, group_lv2 in df2.groupby('type'):
            for name_lv3, group_lv3 in group_lv2.groupby(['type', 'check_item']):
                for table in group_lv3['table_name'].values.tolist():
                    # 数据库表
                    tree.append({'key': table, 'parent': name_lv3[1]})
                    
                # 数据标准
                tree.append({
                    'key': group_lv3['check_item'].values.tolist()[0],
                    'parent': name_lv2,
                })
            # 数据标准分类
            tree.append({
                'key': name_lv2,
            })
            
        return JsonResponse({'data': tree, 'code': 1000})
    except Exception as e:
        return JsonResponse({'data': str(e), 'code': 1001})
    finally:
        engine.dispose()
        

'''echarts使用的json数据
lv1 = []
for name_lv1, group_lv1 in df.groupby('source_system'):
    lv2 = []
    for name_lv2, group_lv2 in df[df['source_system']==name_lv1].groupby(['source_system', 'type']):
        lv3 = []
        for name_lv3, group_lv3 in df[(df['source_system']==name_lv2[0]) & (df['type']==name_lv2[1])].groupby(['source_system', 'type', 'check_item']):
            t = []
            for table in group_lv3['table_name'].values.tolist():
                t.append({'name': table})
                
            lv3.append({
                'name': group_lv3['check_item'].values[0],
                'children': t
            })
        lv2.append({
            'name': name_lv2[1],
            'children': lv3,
        })
    lv1.append({
        'name': name_lv1,
        'children': lv2
    })
    
data = {
    'name': '风险集市',
    'children': lv1
}

with open('1.json', 'w') as f:
    f.write(json.dumps(data))
'''

    