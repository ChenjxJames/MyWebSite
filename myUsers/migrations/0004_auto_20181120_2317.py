# Generated by Django 2.1.2 on 2018-11-20 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myUsers', '0003_auto_20181120_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uPassword',
            field=models.CharField(max_length=32, verbose_name='用户登录密码'),
        ),
    ]
