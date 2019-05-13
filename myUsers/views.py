import time
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from base import MD5
from myUsers import models


# 主页（用户管理页面预留）
def index(request):
    pass


# 登录（验证登录，写入session）
def login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        keep_login = bool(request.POST.get('keeplogin', False))
        try:
            userObj = models.UserInfo.objects.get(uLoginName=username)
            if userObj.uPassword == MD5.get_str_md5(password) and userObj.uEnabled:
                request.session['userid'] = models.UserInfo.objects.get(uLoginName=username).uId
                request.session['username'] = username
                request.session['password'] = password
                request.session.set_expiry(0)
                increase_user_login_info(request)
                # 保持登录一个月
                if keep_login:
                    request.session.set_expiry(30 * 24 * 60 * 60)
                result = {'state': '0', 'info': '登录成功！'}
            else:
                result = {'state': '-111', 'info': '登录失败，用户名或密码错误！'}
        except Exception as err:
            print(err)
            result = {'state': '-112', 'info': '登录失败，用户名或密码错误！'}
        return JsonResponse(result, safe=False)

    else:
        # 检查是否有session保持登录
        if 'username' in request.session and 'password' in request.session:
            username = request.session['username']
            password = request.session['password']
            try:
                userObj = models.UserInfo.objects.get(uLoginName=username)
                if userObj.uPassword == MD5.get_str_md5(password) and userObj.uEnabled:
                    increase_user_login_info(request)
                    return HttpResponseRedirect('/')
            except Exception as err:
                print(err)
        return render(request, 'myUsers/login.html')


# 注销（删除session）
def logout(request):
    if request.method == "GET":
        if 'username' in request.session and 'password' in request.session:
            del request.session['username']
            del request.session['password']
        return HttpResponseRedirect('/user/login')


# 注册（验证用户名是否已被使用，注册成功，跳转登录页面）
def register(request):
    if request.method == "POST":
        registerkey = request.POST.get('registerkey', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')  # 后端再次md5加密
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        try:
            if models.UserInfo.objects.filter(uLoginName=username):
                result = {'state': '-121', 'info': '该用户名已有人使用！'}
            elif models.RegisterKeyInfo.objects.filter(rId=registerkey):
                registerKeyObj = models.RegisterKeyInfo.objects.get(rId=registerkey)
                registerKeyObj.delete()
                u_id = time.strftime('%Y%m%d', time.localtime(time.time())) + "00"
                while True:
                    if len(models.UserInfo.objects.filter(uId=u_id)) == 0:
                        break
                    u_id = str(int(u_id) + 1)

                if models.UserInfo.objects.create(uId=u_id, uLoginName=username, uPassword=MD5.get_str_md5(password),
                                                  uName=name, uEmail=email, uAuthorization=0, uEnabled=True):
                    result = {'state': '0', 'info': '注册成功!'}
                else:
                    result = {'state': '-122', 'info': '注册失败，请联系管理员!'}
            else:
                result = {'state': '-123', 'info': '注册失败，请输入正确的邀请码!'}
        except Exception as err:
            print(err)
            result = {'state': '-4', 'info': '服务器错误，请联系管理员!'}
        return JsonResponse(result, safe=False)

    else:
        return render(request, 'myUsers/register.html')


def set_password(request):
    if request.method == "POST":
        username = get_username(request)
        password = request.POST.get('password', None)  # 后端再次md5加密
        newpassword = request.POST.get('newPassword', None)  # 后端再次md5加密
        try:
            userObj = models.UserInfo.objects.get(uLoginName=username)
            if userObj.uPassword == MD5.get_str_md5(password) and userObj.uEnabled:
                userObj.uPassword = MD5.get_str_md5(newpassword)
                userObj.save()
                result = {'state': '0', 'info': '密码更改成功！'}
            else:
                result = {'state': '-131', 'info': '旧密码输入错误！'}
        except Exception as err:
            print(err)
            result = {'state': '-4', 'info': '服务器错误，请联系管理员!'}
        return JsonResponse(result, safe=False)
    else:
        return render(request, 'myUsers/change_password.html')


# 记录用户登录信息（用户id，登录时间，登录IP）
def increase_user_login_info(request):
    uId = get_userid(request)
    ip = request.META['REMOTE_ADDR']
    models.UserLoginInfo.objects.create(uId=uId, uLoginIP=ip)


# 获取用户信息（返回request的用户名及ID，json格式）
def get_user_info(request):
    result = {'username': get_username(request), 'userId': get_userid(request)}
    return JsonResponse(result, safe=False)


# 获取用户名（返回request的用户名）
def get_username(request):
    if 'username' in request.session:
        return request.session['username']


# 获取用户编号（返回request来自的用户编号）
def get_userid(request):
    if 'userid' in request.session:
        return request.session['userid']


# 判断用户是否登录的函数修饰器（未登录则重定向登录页面，登陆后返回；登录则直接运行函数）
def is_login(fn):
    def inner(request, *args, **kwargs):
        if 'username' in request.session and models.UserInfo.objects.get(uLoginName=get_username(request)).uEnabled:
            return fn(request, *args, **kwargs)
        else:
            # 如果用户未登录，301重定向到登录界面
            return login(request)

    return inner
