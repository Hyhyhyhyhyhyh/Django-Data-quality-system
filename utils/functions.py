from functools import wraps
from django.shortcuts import redirect


class is_login():
    '''从session判断发起请求的账号是否已经登录，session中未有登录信息则跳转到登录界面
    '''
    def __new__(self, func):
        @wraps(func)
        def _wrap(request):
            if request.session.get('is_login') is None or request is None:
                return redirect("../../authorize/login")
            else:
                f = func(request)
                return f

        return _wrap