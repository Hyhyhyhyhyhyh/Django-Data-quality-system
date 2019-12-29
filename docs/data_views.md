# 数据质量仪表盘接口

## index
- URL：http://100.100.0.177/data/index

- 功能：重定向到http://100.100.0.177/data/dashboard
- 请求类型：GET
- 请求参数：无
- 返回值：无

---

## dashboard
- URL：http://100.100.0.177/data/dashboard

页面内容：
1. 集团数据质量总览：检核数据总量、问题数据总量总问题占比
    - `ajax请求api/data_overiew`
2. 选定季度的数据质量问题概况，7家子公司明细
    - `ajax请求api/avg_problem_percentage`
3. 所有季度的各公司平均问题占比，柱状图
4. 所有季度的集团总问题占比，折线图
    - `ajax请求api/total_trend`
5. 选定季度的需求改造进度统计，柱状图
    - `ajax请求api/demand/list_subcompany`
6. 选定季度的需求改造进度统计，表格
    - `ajax请求api/demand/list_subcompany`
7. 选定季度的各公司数据量占比，环状图
    - `ajax请求api/subcompany_data_percentage获取各公司数据量`
    - `ajax请求api/count_db_rows获取各类型数据库数据量`
8. 各公司同类问题Top 5统计，饼图
    - `ajax请求api/same_problem_top5`
9. 风险集市指标统计，图片
    - `手工置换/data/data-quality/static/resource/风险集市指标统计.png`

- 请求类型：GET
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
quarter | 非必须 | 选择显示的季度，不传入则显示上一季度的数据

- 返回值：无

--- 

## dashboard_subcompany
- URL：http://100.100.0.177/data/dashboard_subcompany

页面内容：
1. 选定季度的子公司问题数据项统计，柱状图及列表
    - `ajax调用data/subcompany_problem_count`\
2. 子公司源系统改造情况
    - `ajax请求api/demand/list_subcompany`
3. 子公司风险指标，图片及下载excel
    - `图片手工置换服务器/data/data-quality/static/resource/XX公司风险指标.png`
    - `ajax请求api/files/download下载对应公司的指标Excel表`

- 请求类型：GET
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
name    | 必须   | 子公司简写
company | 必须   | 子公司中文简写
quarter | 非必须 | 选择显示的季度，不传入则显示上一季度的数据

- 返回值：无

--- 

## result_detail
- URL：http://100.100.0.177/data/result_detail
- 页面内容：选定季度的数据质量检核报告Excel结果
- 请求类型：GET
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
name    | 必须   | 子公司简写
quarter | 非必须 | 选择显示的季度，不传入则显示上一季度的数据
- 返回值：无

--- 

## report
- URL：http://100.100.0.177/data/report
- 页面内容：选定季度的数据质量检核报告Word结果，结果还需要人工加工
- 请求类型：GET
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
quarter | 非必须 | 选择显示的季度，不传入则显示上一季度的数据
- 返回值：无
