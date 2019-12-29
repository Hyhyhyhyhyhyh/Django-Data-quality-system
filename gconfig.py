# from gevent import monkey
# monkey.patch_all()

import multiprocessing, logging

debug        = True
timeout      = 2000                     # 超时时间
bind         = '0.0.0.0:9000'         # 提供web服务的端口，如果要跟容器通信，ip不能设置为localhost或127.0.0.1
backlog      = 2048                     # 监听队列
chdir        = '/data/pyweb/data-quality'
threads      = multiprocessing.cpu_count() * 2   # 指定每个进程开启的线程数，实际并发数为workers * threads
workers      = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"                 # 默认为阻塞sync模式（不设置threads为单线程），使用协程选择gevent模式

# 日志设置
loglevel          = 'debug'
pidfile           = '/data/pyweb/data-quality/logs/gunicorn.pid'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"' 
errorlog          = "/data/pyweb/data-quality/logs/gunicorn_error.log"        # 错误日志文件
capture_output    = True
accesslog         = '-'