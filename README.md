# demo
http://www.sghen.cn:9000

# 启停项目
```
# 切换虚拟环境
workon django-2.1

# 启动项目
gunicorn mysite.wsgi -c /data/pyweb/data-quality/gconfig.py

# 停止项目
gunicorn mysite.wsgi -c /data/pyweb/data-quality/gconfig.py
```

# 更新记录
## 2019-12-29
实际部署demo

## 2019-09-09
demo

# 前端效果（demo版本）
![数据质量仪表盘_1](https://github.com/Hyhyhyhyhyhyh/django-Data-quality-check-system/blob/master/%E4%BB%AA%E8%A1%A8%E7%9B%981.png)
![数据质量仪表盘_2](https://github.com/Hyhyhyhyhyhyh/django-Data-quality-check-system/blob/master/%E4%BB%AA%E8%A1%A8%E7%9B%982.png)
![数据质量检核报告word](https://github.com/Hyhyhyhyhyhyh/django-Data-quality-check-system/blob/master/%E6%95%B0%E6%8D%AE%E8%B4%A8%E9%87%8F%E6%8A%A5%E5%91%8A.png)
![数据质量检核结果明细excel_1](https://github.com/Hyhyhyhyhyhyh/django-Data-quality-check-system/blob/master/%E6%A3%80%E6%A0%B8%E6%98%8E%E7%BB%861.png)
![数据质量检核结果明细excel_2](https://github.com/Hyhyhyhyhyhyh/django-Data-quality-check-system/blob/master/%E6%A3%80%E6%A0%B8%E6%98%8E%E7%BB%862.png)
![数据质量检核规则库](https://github.com/Hyhyhyhyhyhyh/django-Data-quality-check-system/blob/master/%E6%A3%80%E6%A0%B8%E8%A7%84%E5%88%99%E5%BA%93.png)
![添加或编辑检核规则](https://github.com/Hyhyhyhyhyhyh/django-Data-quality-check-system/blob/master/%E6%B7%BB%E5%8A%A0%E6%88%96%E7%BC%96%E8%BE%91%E6%A3%80%E6%A0%B8%E8%A7%84%E5%88%99.png)
![自动检核](https://github.com/Hyhyhyhyhyhyh/django-Data-quality-check-system/blob/master/%E8%87%AA%E5%8A%A8%E6%A3%80%E6%A0%B8.png)
