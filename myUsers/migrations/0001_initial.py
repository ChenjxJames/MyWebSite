# Generated by Django 2.1.2 on 2018-11-20 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('uId', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='用户编号')),
                ('uLoginName', models.CharField(max_length=10, unique=True, verbose_name='用户登录名')),
                ('uPassword', models.CharField(max_length=255, verbose_name='用户登录密码')),
                ('uName', models.CharField(max_length=10, verbose_name='用户姓名')),
                ('uEamil', models.EmailField(max_length=255, verbose_name='用户邮箱地址')),
                ('uRegisterTime', models.DateTimeField(verbose_name='用户注册时间')),
                ('uLastLoginTime', models.DateTimeField(verbose_name='用户上次登录时间')),
                ('uAuthorization', models.IntegerField(verbose_name='用户权限')),
            ],
        ),
    ]
