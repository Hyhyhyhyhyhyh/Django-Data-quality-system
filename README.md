# demo
http://data.sghen.cn
登录用户名密码：admin/admin

# 项目结构
```
项目
│  gconfig.py                               gunicorn配置文件
│  manage.py                                Django管理文件
│  README.md                                readme
|  nginx.conf                               nginx.conf
│
├─api
│     api_dashboard.py                      仪表盘api接口
│     api_datastandard.py                   数据标准api接口
│     api_files.py                          文件下载api接口
│
├─authorize
│  │  views.py                              登录验证模块代码
│  └─templates
│      └─authorize
│              login.html                   前端HTML模板
│
├─check
│  │  autocheck.py                          执行自动检核代码
│  │  crontab.py                            自动检核定时任务管理代码
│  │  crontab_autocheck.py                  执行自动检核定时任务代码
│  │  functions.py                          查询检核进度
│  │  views.py                              检核模块代码
│  └─templates
│      └─check
│              rule_add.html                添加检核规则页面模板
│              rule_config.html             编辑检核规则页面模板
│              rule_exec.html               手工执行检核页面模板
│              rule_list.html               查看检核规则列表页面模板
│              show_crontab.html            查看自动检核定时任务页面模板
│
├─data
│  │  views.py                              仪表盘+检核结果显示模板代码
│  └─templates
│      └─data
│              dashboard.html               集团仪表盘页面模板
│              dashboard_subcompany.html    子公司仪表盘页面模板
│              index.html
│              report.html                  自动生成的word检核报告页面模板
│              result_detail.html           检核报告excel页面模板
│              template-ui.html             ***UI模板***
│
├─demand
│  │  insert_excel.sql
│  │  views.py                              源系统改造需求excel模块代码
│  └─templates
│      └─demand
│              upload_form.html             源系统改造需求excel表上传页面
│
├─docs                                      文档目录
│      api_views.md
│      authorize_views.md
│      check_views.md
│      data_views.md
│      ddl.sql                              一些数据库表的DDL语句
│      demand_views.md
│      files_views.md
│      部署文档.md
│      requirements.txt                     python项目的库列表
│
├─files
│  │  views.py                             数据治理知识库模块代码 
│  └─templates
│      └─files
│              file_list.html               数据治理知识库页面模板
│
├─logs                                      错误日志
├─mysite
│      db_config.py                         记录检核结果的本地数据库配置文件
│      settings.py                          Django框架配置文件
│      source_db_config.py                  源系统数据库配置文件
│      urls.py                              url路由配置文件
│      wsgi.py
│
├─standard
│  │  views.py                              数据标准模块代码
│  └─templates
│      └─standard
│              show.html                    查看数据标准页面
│              update.html                  编辑数据标准页面
|
├─utils                                     一些复用的函数
│     query.py
|     report_data.py
│
└─static                                    css、js、附件等静态文件目录
```


# 更新记录
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
- [ ] 使用pandas方法精细化检核逻辑
- [ ] 数据标准编辑功能完善