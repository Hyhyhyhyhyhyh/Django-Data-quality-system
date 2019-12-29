from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from crontab import CronTab

def show_crontab(request):
    if request.session.get('is_login',None) is None:
        return redirect("../../authorize/login")
    
    username = request.session['username']
    cron  = CronTab(user=True)
    job = list(cron.find_comment('自动进行数据质量检核'))[0]    # 根据comment查询crontab
    if job.is_enabled() is True:
        job_time = str(job).split('#')[0][0:9]
    else:
        job_time = str(job).split('#')[1][1:10]
    return render(request,"check/show_crontab.html",{"username": username,
                                                     "status": str(job.is_enabled()),
                                                     "job_name": job.comment,
                                                     "job_command": job.command,
                                                     "job_time": job_time,
                                                     "last_run": str(job.last_run),
                                                    }
                )
    

def enable_crontab(request):
    status = request.POST.get('status')
    
    cron  = CronTab(user=True)
    job = list(cron.find_comment('自动进行数据质量检核'))[0]
    
    if status == 'false':
        # job.enable(False)
        # cron.write()
        return  JsonResponse({"msg": "操作成功"})
    elif status == 'true':
        # job.enable()
        # cron.write()
        return  JsonResponse({"msg": "操作成功"})
    else:
        return  JsonResponse({"msg": "操作失败"})
    

def update_crontab(request):
    job_time = request.POST.get('job_time')
    
    try:
        # cron  = CronTab(user=True)
        # job = list(cron.find_comment('自动进行数据质量检核'))[0]
        # job.setall(job_time)
        return JsonResponse({"msg": "操作成功"})
    except Exception as e:
        return JsonResponse({"msg": "操作失败", "reason": e})