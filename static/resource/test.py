import cx_Oracle,os,json

def rule_detail(company,filter):
    #company=request.POST.get('name')
    #filter=request.POST.get('risk_market')
    #连接数据库
    os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.UTF8'
    conn = cx_Oracle.connect('result/result@100.100.0.177:4998/checkdb')
    curs = conn.cursor()
    sql = "select id,check_item,target_table,risk_market_item,problem_type,check_sql,note from check_result_template where source_system in ('"+company+"') order by id"
    print(sql)
    rr = curs.execute (sql)
    result = curs.fetchall()
    #构造json
    id               = [i[0] for i in result]
    check_item       = [i[1] for i in result]
    target_table     = [i[2] for i in result]
    risk_market_item = [i[3] for i in result]
    problem_type     = [i[4] for i in result]
    check_sql        = [i[5] for i in result]
    note             = [i[6] for i in result]
    result_dict = dict(zip(id,check_item,target_table,risk_market_item,problem_type,check_sql,note))
    print (json.dumps(result_dict))