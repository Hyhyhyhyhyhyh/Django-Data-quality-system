// 设置随机背景图
function Onload(){
    var imgList = [
        "/static/img/bg_0.jpg",
        "/static/img/bg_1.jpg",
        "/static/img/bg_2.jpg",
    ]
    var imgRandom = Math.floor(Math.random() * (imgList.length));
    html = "<div id=\"bg-pict\" style=\"background-image:url(/static/img/bg_" + imgRandom + ".jpg);\"></div>"
    imgRandom = Math.floor(Math.random() * imgList.length);
    html += "<div id=\"bg-pict\" style=\"background-image:url(/static/img/bg_" + imgRandom + ".jpg);\"></div>"
    imgRandom = Math.floor(Math.random() * imgList.length);
    html += "<div id=\"bg-pict\" style=\"background-image:url(/static/img/bg_" + imgRandom + ".jpg);\"></div>"
    document.getElementById("bg").innerHTML = html;
}


// 登录验证
function Login() {
    document.getElementById("login").disabled = true;
    $.ajax({
        url: "../../authorize/login_auth",
        type: "POST",
        dataType: "json",
        data: {
            username: $("#username").val(),
            password: $("#password").val(),
        },
        success: function (data) {
            if (data.status == 'success') {
                swal({
                    title: "欢迎回来!",
                    text: "正在跳转...",
                    icon: "success",
                    buttons: false,
                    timer: 1000,
                }).then(function(){
                    window.location.href = '../../data/dashboard/';
                });
            }
            else {
                document.getElementById("login").disabled = false;
                swal("登录失败!", data.status, 'error');
            }
        },
        error: function () {
            document.getElementById("login").disabled = false;
        }
    });
}

function NextElement(id){
    if ( id == 'username' && event.keyCode == 13 ){
        document.getElementById("password").focus();
    }
    else if ( id == 'password' && event.keyCode == 13 ){
        document.getElementById("login").click();
    }
    else if ( id == 'send-sms' && event.keyCode == 13 ){
        document.getElementById("new-password").focus();
    }
    else if ( id == 'new-password' && event.keyCode == 13 ){
        document.getElementById("reset").click();
    }
}


// 发送短信
function SendSMSCode(){
    if ( $("#mobile").val() == '' || $("#mobile").val() == null ){
        swal({
            text: '请先输入手机号',
            icon: 'warning',
            buttons: false,
            timer: 1000,
        })
        return;
    }
    $.ajax({
        url: "",
        type: "GET",
        dataType: "json",
        contentType:'application/x-www-form-urlencoded',
        data: {
            mobile: $("#mobile").val(),
        },
        success: function (data) {
            if ( data.status == '短信发送成功' ){
                swal({
                    'text': '短信发送成功',
                    'icon': 'success',
                    'buttons': false,
                    'timer': 1000
                });
                var obj = $("#send-sms");
                $("#sms-code").focus();
                settime(obj);
            }
            else if ( data.status == '验证失败' ) {
                swal({
                    title: data.status,
                    text: data.msg,
                    icon: 'error'
                });
            }
            else {
                swal({
                    title: data.status,
                    text: data.msg,
                    icon: 'error'
                });
            }
        },
        error: function () {
            swal({
                text: '服务器正在开小差，请稍候重试...',
                icon: 'warning'
            });
        }
    });
    
}


// 验证码有效期
var countdown=60; 
function settime(obj) { //发送验证码倒计时
    if (countdown == 0) { 
        obj.attr('disabled',false); 
        obj.html("获取验证码");
        countdown = 60; 
        return;
    } else { 
        obj.attr('disabled',true);
        obj.html("重新发送(" + countdown + ")...");
        countdown--; 
    } 
setTimeout(function() { 
    settime(obj) }
    ,1000) 
}


// 登录框键入回车换行
function SwitchTab(id){
    if ( id == 'InputForm' ){
        document.getElementById("InputForm").style.display='block';
        document.getElementById("ResetForm").style.display='none';
        document.getElementById("reset-pwd").className='';
        document.getElementById("login-page").className='active';
        document.getElementById("login").style.display='unset';
        document.getElementById("reset").style.display='none';
    }
    else if ( id == 'ResetForm' ){
        document.getElementById("ResetForm").style.display='block';
        document.getElementById("InputForm").style.display='none';
        document.getElementById("reset-pwd").className='active';
        document.getElementById("login-page").className='';
        document.getElementById("login").style.display='none';
        document.getElementById("reset").style.display='unset';
    }
}


// 修改密码
function ModifyPassword() {
    document.getElementById("login").disabled = true;
    $.ajax({
        url: "",
        type: "POST",
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        dataType: "json",
        contentType:'application/x-www-form-urlencoded',
        data: {
            mobile: $("#mobile").val(),
            code: $("#sms-code").val(),
            password: $("#new-password").val(),
        },
        success: function (data) {
            var user = data.username;
            if (data.status == '修改成功') {
                swal({
                    title: "重置密码成功!",
                    text: "正在跳转...",
                    icon: "success",
                    buttons: false,
                    timer: 1000,
                }).then(function(){
                    window.location.href = 'portal.html#token=' + data.token;
                });
            }
            else if ( data.status == '验证码错误' ){
                swal({
                    title: "验证码错误",
                    icon: "error",
                }).then(function(){
                    document.getElementById("login").disabled = false;
                });
            }
            else {
                document.getElementById("login").disabled = false;
                swal("登录失败!", data.reason, 'error');
            }
        },
        error: function () {
            document.getElementById("login").disabled = false;
        }
    });
}