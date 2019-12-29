import requests, datetime, math, threading

quarter = str(datetime.datetime.now().year)+"Q"+str(math.ceil(datetime.datetime.now().month/3.))
url = "http://dataquality.utrustfintech.com/check/rule_execute"

def post_rule_execute(company, quarter):
    data = {'company': company, 'username': 'crontab', 'quarter': quarter}
    r = requests.post(url, data)

t1 = threading.Thread(target=post_rule_execute, args=('ycxt', quarter))
t2 = threading.Thread(target=post_rule_execute, args=('yczc', quarter))
t3 = threading.Thread(target=post_rule_execute, args=('gdzdb', quarter))
t4 = threading.Thread(target=post_rule_execute, args=('ycjk', quarter))
t5 = threading.Thread(target=post_rule_execute, args=('fdct', quarter))
t6 = threading.Thread(target=post_rule_execute, args=('zyyc', quarter))
t7 = threading.Thread(target=post_rule_execute, args=('jz', quarter))

t1.start();t2.start();t3.start();t4.start();t5.start();t6.start();t7.start()

# 等待运行结束
t1.join();t2.join();t3.join();t4.join();t5.join();t6.join();t7.join()

