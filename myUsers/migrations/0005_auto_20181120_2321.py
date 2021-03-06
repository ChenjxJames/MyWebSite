# Generated by Django 2.1.2 on 2018-11-20 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myUsers', '0004_auto_20181120_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uLastLoginTime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='用户上次登录时间'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='uRegisterTime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='用户注册时间'),
        ),
    ]
