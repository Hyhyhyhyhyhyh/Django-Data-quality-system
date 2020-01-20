from django.shortcuts import render

from utils.functions import is_login


@is_login
def show(request):
    return render(request, "standard/show.html",
                  {"username": request.session.get('username')})


@is_login
def update(request):
    return render(
        request, "standard/update.html", {
            "username": request.session.get('username'),
            "std_name": request.GET.get('std_name'),
            "std_type": request.GET.get('std_type'),
        })
