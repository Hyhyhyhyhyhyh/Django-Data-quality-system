# demo
http://data.sghen.cn
登录用户名密码：admin/admin

# 项目结构
```
项目
│  gconfig.py           gunicorn配置文件
│  manage.py            Django管理文件
│  README.md            readme
|  nginx.conf           nginx.conf
│
├─api                   ajax接口
│
├─authorize             身份认证模块
|
├─check                 自动检核模块
|
├─data                  仪表盘、检核明细模块
|
├─demand                更新源系统改造需求
|
├─docs                  文档目录
│
├─files                 上传下载文件模块
│
├─logs                  日志目录
|
├─mysite                Django配置目录
│
├─standard              查看、更新数据标准模块
|
├─utils                 一些复用的函数
│
└─static                css、js、附件等静态文件目录
```


# 更新记录
## 2020-09-05
- 修复若干本地部署会发生的错误
- **重要**：修正部署文档`docs/部署文档.md`中的许多错误

## 2020-06-13
- 更新血缘分析模块

## 2020-05
- 数据源跟检核规则库中的数据库进行关联

## 2020-04-23
1. 前端侧边栏修改，显示更加紧凑
2. 新增数据源的查看/修改/新增功能


## 2020-03-29
1. 后端
    - 检核结果由按季度存放改在按日存放，记录检核版本方便查看历史变化趋势
    - 根据check_execute_log检核日志表为前端提供日期选择接口；api代码更新为正式代码（代替随机数据）
    - 添加日期维度表
2. 前端：在仪表盘添加各公司质量总览及全期趋势图；添加日期选择控件等
3. 进一步前后分离，减少后端渲染模板

## 2019-12-29
实际部署demo

## 2019-09-09
demo


# 启停项目
```
# 切换虚拟环境
workon django-2.1

# 启动项目
gunicorn mysite.wsgi -c /data/pyweb/data-quality/gconfig.py &
```

# todo
- [ ] 数据标准编辑功能完善

# 说明
登录页面背景图来自https://pixabay.com