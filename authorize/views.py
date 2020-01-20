from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


# from ldap3 import Server, Connection, ALL, SUBTREE, ServerPool,ALL_ATTRIBUTES

# 登录页面
def login(request):
    return render(request, "authorize/login.html")


# 登录验证
@require_http_methods(["POST"])
def login_auth(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    # 普通验证
    if username == 'admin' and password == 'admin':
        request.session['username'] = username
        request.session['is_login'] = True
        return redirect('../../data/index')
    else:
        # user_conn.unbind()
        # conn.unbind()
        alert = "<script>alert ('登录信息不正确');window.location.href='login';</script>"
        return render(request, 'authorize/login.html', {'alert': alert})

    """
    使用openLDAP进行用户身份验证

    server = Server(host='', port=636, use_ssl=True, get_info='ALL')
    # 使用admin登录openldap验证输入的用户名
    ldap_admin_dn = ""
    ldap_admin_password = ""
    conn = Connection(server, user=ldap_admin_dn, password=ldap_admin_password, auto_bind=True,version=3)
    res = conn.search(search_base='',search_filter='(uid={})'.format(username)) #验证表单输入的账号名
    if res:
        entry = conn.response[0]  # 验证账号名及获取用户组织架构
        user_dn = entry['dn']
        user_status = entry['attributes']  #后续增加账号状态验证
        # 验证密码
        user_conn = Connection(server, user=user_dn, password=password, auto_bind=False,version=3)
        if user_conn.bind() is True:
            #验证通过
            user_conn.unbind()
            conn.unbind()
            
            if request.POST.get('autologin')=="1":
                request.session.set_expiry(7*24*60*60)  #session过期时间为7天
            request.session['username']=username
            request.session['is_login']=True
            return redirect('../../data/index')
        else:
            user_conn.unbind()
            conn.unbind()
            alert = "<script>alert ('密码输入不正确');window.location.href='login';</script>"
            return render(request, 'authorize/login.html',{'alert':alert})
    else:
        conn.unbind()
        alert = "<script>alert ('账号名输入不正确');window.location.href='login';</script>"
        return render(request, 'authorize/login.html',{'alert':alert})
    """


def logout(request):
    request.session.clear()
    return render(request, "authorize/login.html")
