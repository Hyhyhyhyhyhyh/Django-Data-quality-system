# 身份验证接口

## login
- URL：http://100.100.0.177/authorize/login

- 功能：登录表单，用户输入账号名密码
- 请求类型：GET
- 请求参数：无
- 返回值：无

---

## login_auth
- URL：http://100.100.0.177/authorize/login_auth

- 功能：连接LDAP，验证login页面表单post传递的用户名密码
- 请求类型：POST / GET
- 请求参数：

参数 | 是否必须 | 说明
-|-|-
username | 必须 | OA账号名
password | 必须 | OA账号密码

- 返回值：验证成功自动重定向到主页，并在服务端记录session；否则返回报错信息（用户名/密码输入错误）

---

## logout
- URL：http://100.100.0.177/authorize/logout

- 功能：清除用户对应的session，重定向到登录login页
- 请求类型：GET
- 请求参数：无
- 返回值：无