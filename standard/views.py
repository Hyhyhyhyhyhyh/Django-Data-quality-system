from django.shortcuts import render, redirect

def show(request):
    if request.session.get('is_login',None) is None:
        return redirect("../../authorize/login")
    
    return render(request,"standard/show.html",{"username": request.session.get('username'),
                })

def update(request):
    if request.session.get('is_login',None) is None:
        return redirect("../../authorize/login")

    return render(request,"standard/update.html",{"username": request.session.get('username'),
                                                  "std_name": request.GET.get('std_name'),
                                                  "std_type": request.GET.get('std_type'),
                })