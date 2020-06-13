"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from django.views.generic import RedirectView
from django.views.static import serve
from django.conf.urls import url

from data import views as dataView
from authorize import views as authView
from check import views as checkView
from demand import views as demandView
from files import views as filesView
from standard import views as stdView
from backend import views as beView
from blood import views as bloodView
from api import api_files as api_filesView
from api import api_dashboard as api_dashView
from api import api_datastandard as api_stdView
from api import api_check as api_checkView
from api import api_date as api_dateView
from api import api_quality as api_qualityView
from api import api_backend as api_beView
from api import api_blood as api_bloodView

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve, {'document_root': '/data/pyweb/data-quality/static'}, name='static'),

    # 仪表盘
    path('data/dashboard/',             dataView.dashboard,                   name='dashboard'),
    path('data/dashboard/subcompany',   dataView.dashboard_subcompany,        name='dashboard_subcompany'),
    path('data/report',                dataView.report,                      name='report'),
    path('data/result_detail',         dataView.result_detail,               name='result_detail'),
    path('',                            RedirectView.as_view(url='data/dashboard/')),
    path('data',                        RedirectView.as_view(url='data/dashboard/')),
    path('data/index',                  RedirectView.as_view(url='../data/dashboard/')),

    # 登录身份验证
    path('authorize/login/',     authView.login,      name='login'),
    path('authorize/logout/',    authView.logout,     name='logout'),
    path('authorize/login_auth', authView.login_auth, name='login_auth'),

    # 检核
    path('check/rule',          checkView.rule_list,            name='rule'),
    path('check/rule/edit',     checkView.rule_edit,            name='rule_edit'),
    path('check/rule/exec',     checkView.rule_execute_manual,  name='rule_execute_manual'),
    # 检核定时任务
    path('check/crontab',       checkView.show_crontab,        name='show_crontab'),
    # 血缘分析
    path('blood/analyze',       bloodView.analyze,      name='blood_analyze'),

    # 源系统改造需求
    path('demand/import_sheet', demandView.import_sheet, name='import_sheet'),

    # 附件管理
    path('files/list', filesView.list, name='files_list'),

    # 数据标准
    path('datastandard/show',   stdView.show,   name='std_show'),
    path('datastandard/update', stdView.update, name='update'),
    
    # 后台管理
    path('backend/database',   beView.database,    name='database'),
    path('backend/database/detail',   beView.database_detail,    name='database_detail'),
    path('backend/database/add',   beView.database_add,    name='database_add'),
    path('backend/crontab',   beView.crontab,    name='crontab'),

    # API
    path('api/date/year',       api_dateView.year_list,     name='year_list'),
    path('api/date/quarter',    api_dateView.quarter_list,  name='quarter_list'),
    path('api/date/month',      api_dateView.month_list,    name='month_list'),
    path('api/date/day',        api_dateView.day_list,      name='day_list'),
    
    path('api/demand/list_subcompany',               demandView.list_subcompany,              name='demand_list_subcompany'),
    path('api/files/download',                       api_filesView.download,                  name='files_download'),

    path('api/dashboard/avg_problem_percentage',     api_dashView.avg_problem_percentage,     name='avg_problem_percentage'),
    path('api/dashboard/same_problem_top5',          api_dashView.same_problem_top5,          name='same_problem_top5'),
    path('api/dashboard/count_db_rows',              api_dashView.count_db_rows,              name='count_db_rows'),
    path('api/dashboard/data_overview_total',        api_dashView.data_overview_total,        name='data_overview_total'),
    path('api/dashboard/data_overview_company',      api_dashView.data_overview_company,      name='data_overview_company'),
    path('api/dashboard/total_trend',                api_dashView.total_trend,                name='total_trend'),
    path('api/dashboard/subcompany_problem_count',   api_dashView.subcompany_problem_count,   name='subcompany_problem_count'),
    path('api/dashboard/subcompany_data_percentage', api_dashView.subcompany_data_percentage, name='subcompany_data_percentage'),
    path('api/dashboard/data_overview_company_trend', api_dashView.data_overview_company_trend, name='data_overview_company_trend'),

    path('api/datastandard/query/detail',            api_stdView.query_detail,                name='query_detail'),
    path('api/datastandard/update',                  api_stdView.update,                      name='update'),
    path('api/datastandard/query/index',             api_stdView.query_index,                 name='query_index'),
    path('api/datastandard/query/history',           api_stdView.query_update_history,        name='query_update_history'),
    
    path('api/check/rule',                           api_checkView.rule,                      name='api_rule'),
    path('api/check/rule/detail',                    api_checkView.rule_detail,               name='rule_detail'),
    path('api/check/rule/update',                    api_checkView.rule_update,               name='rule_update'),
    path('api/check/rule/add',                       api_checkView.rule_add,                  name='rule_add'),
    path('api/check/rule/status_modify',             api_checkView.rule_status_modify,        name='rule_status_modify'),
    path('api/check/rule/execute',                   api_checkView.rule_execute,              name='rule_execute'),
    path('api/check/progress',                       api_checkView.query_check_progress,      name='query_check_progress'),
    
    # 检核结果明细
    path('api/quality/detail',                       api_qualityView.quality_detail,          name='quality_detail'),
    path('api/quality/report',                       api_qualityView.report_detail,           name='report_detail'),
    
    path('api/backend/database/query',           api_beView.db_query,        name='db_query'),
    path('api/backend/database/update',           api_beView.db_update,        name='db_update'),
    path('api/backend/database/insert',           api_beView.db_insert,        name='db_insert'),
    path('api/backend/crontab/enable',          api_beView.crontab_enable,            name='crontab_enable'),
    path('api/backend/crontab/run',          api_beView.crontab_run,            name='crontab_run'),
    
    path('api/blood/mapping',                  api_bloodView.query_mapping,             name='api_blood_query_mapping'),
]
