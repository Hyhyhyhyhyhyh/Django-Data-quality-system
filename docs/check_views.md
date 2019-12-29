# 自动检核说明

## rule_list
- URL：http://100.100.0.177/check/login
- 功能：检核规则库，`规则列表的内容由ajax调用check/rule_detail获取`
- 请求类型：GET
- 请求参数：无
- 返回值：无

---

## rule_status_modify
- URL：http://100.100.0.177/check/rule_status_modify
- 功能：启用或禁用单条检核规则
- 请求类型：POST
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
id          | 必须 | 前端显示的行号
post_status | 必须 | 传入值为`已启用`时，禁用该条规则；传入值为`已禁用`时，启用该条规则
company     | 必须 | 检核规则所属的公司中文简写


- 返回值：无

---

## rule_config
- URL：http://100.100.0.177/check/rule_config
- 功能：查看检核规则详情
- 请求类型：GET
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
id          | 必须 | 前端显示的行号
post_status | 必须 | 传入值为`已启用`时，禁用该条规则；传入值为`已禁用`时，启用该条规则
company     | 必须 | 检核规则所属的公司中文简写
username    | 必须 | 验证修改者身份，OASSO账号无提交按钮

- 返回值：无

---

## rule_exec
- URL：http://100.100.0.177/check/rule_exec
- 功能：查看当前的手工触发的检核进度
- 请求类型：GET
- 请求参数：无
- 返回值：无

---

## rule_detail
- URL：http://100.100.0.177/check/rule_detail
- 功能：获取检核规则内容
- 请求类型：GET
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
name               | 必须 | 子公司简写，与Excel中的系统名一致
risk_market_filter | 必须 | 接受传入的值为`是`或`否`或空
- 示例：http://100.100.0.177/check/rule_detail?name=信托&risk_market_filter=

- 返回值：
```
{
	"data": [{
		"id": 1,
		"check_item": "项目编号",
		"target_table": "项目基本信息",
		"risk_market_item": "是",
		"problem_type": "空值检核",
		"db": "sqlserver",
		"check_sql": "select count(distinct vc_stock_code),\n       count(CASE\n               WHEN vc_stock_code IS NULL or vc_stock_code = '' THEN\n                1\n             END)\n  from (select t.vc_stock_code,\n               t.vc_contract_no,\n               t.en_contract_balance,\n               t.vc_invest_use,\n               t.l_begin_date,\n               t.l_end_date\n               \n          from hswinrun2.dbo.stockcodesex t\n         where t.l_end_date >= '20180101'and t.l_end_date < '20990101'\n        union all\n        select t.vc_stock_code,\n               t.vc_contract_no,\n               t.en_contract_balance,\n               t.vc_invest_use,\n               t.l_begin_date,\n               t.l_end_date\n          from hswinrun2_xedk.dbo.stockcodesex t\n         where t.l_end_date >= '20180101'and t.l_end_date < '20990101') a",
		"note": "",
		"status": "已启用",
		"source_system": "信托"
	}]
}
```

---

## rule_update
- URL：http://100.100.0.177/check/rule_update
- 功能：提交对检核规则的修改
- 请求类型：POST
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
id            | 必须 | 规则对应的行号
source_system | 必须 | 规则所属的子公司中文简写
check_item    | 必须 | 要修改为的`数据标准`名
target_table  | 必须 | 要修改为的`目标表`名
risk_market   | 必须 | `是否风险集市所需指标`，接受的参数为`是`/`否`
problem_type  | 必须 | 要修改为的`问题分类`
db            | 必须 | 要修改为的`源系统数据库`类型
check_sql     | 必须 | 要修改为的`检核逻辑`
note          | 必须 | 要修改为的`备注`
status        | 必须 | 要修改为的`规则启用状态`，接受的参数为`已启用`/`已停用`；传入`已启用`会把规则状态置为启用，传入`已停用`会把规则状态置为禁用

- 返回值：
```
修改成功返回'success'，http状态码200；发生异常则状态码为500
```

---

## rule_add
- URL：http://100.100.0.177/check/rule_add
- 功能：提交对检核规则的新增
- 请求类型：POST
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
source_system | 必须 | 规则所属的子公司中文简写
check_item    | 必须 | 要新增的`数据标准`名
target_table  | 必须 | 要新增的`目标表`名
risk_market   | 必须 | `是否风险集市所需指标`，接受的参数为`是`/`否`
problem_type  | 必须 | 要新增的`问题分类`
db            | 必须 | 要新增的`源系统数据库`类型
check_sql     | 必须 | 要新增的`检核逻辑`
note          | 必须 | 要新增的`备注`
status        | 必须 | 要新增的`规则启用状态`，接受的参数为`已启用`/`已停用`；传入`已启用`会把规则状态置为启用，传入`已停用`会把规则状态置为禁用

- 返回值：
```
新增成功返回'success'，http状态码200；发生异常则状态码为500
```

---

## rule_execute
- URL：http://100.100.0.177/check/rule_execute
- 功能：提交对检核规则的新增
- 请求类型：POST
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
company  | 必须 | 执行检核的公司，接受的参数为`ycxt`/`yczc`/`gdzdb`/`ycjk`/`fdct`/`zyyc`/`jz`
username | 必须 | 执行检核的用户名，用于记录日志
quarter  | 必须 | 检核结果将会落在该季度的表中

- 返回值：
```
{
	"status": "success",
	"msg": "XX公司检核成功！"
}
```