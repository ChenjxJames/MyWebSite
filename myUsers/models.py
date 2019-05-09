from django.db import models


class UserInfo(models.Model):
    """
    用户信息模型类（用户编号， 用户登录名， 用户密码， 用户姓名， 用户邮箱地址， 用户注册时间, 用户权限，用户账户启用标识)
    """
    uId = models.CharField(max_length=10, null=False, verbose_name='用户编号', primary_key=True)
    uLoginName = models.CharField(max_length=10, null=False, verbose_name='用户登录名', unique=True)
    uPassword = models.CharField(max_length=32, null=False, verbose_name='用户登录密码')
    uName = models.CharField(max_length=32, null=False, verbose_name='用户姓名')
    uEmail = models.EmailField(max_length=255, null=False, verbose_name='用户邮箱地址')
    uRegisterTime = models.DateTimeField(auto_now_add=True, verbose_name='用户注册时间')
    uAuthorization = models.IntegerField(null=False, verbose_name='用户权限')
    uEnabled = models.BooleanField(null=False, verbose_name='用户账户启用标识', default=True)


class UserLoginInfo(models.Model):
    """
    用户登录信息模型类（用户编号，登陆时间，登录IP地址）
    """
    uId = models.CharField(max_length=10, null=False, verbose_name='用户编号')
    uLoginTime = models.DateTimeField(auto_now_add=True, null=False, verbose_name='用户登录时间')
    uLoginIP = models.CharField(max_length=15, null=False, verbose_name='用户登录IP地址')


class RegisterKeyInfo(models.Model):
    """
    注册邀请码信息模型类（注册邀请码编号，）
    """
    rId = models.CharField(max_length=32, null=False, verbose_name='注册邀请码编号', primary_key=True)
