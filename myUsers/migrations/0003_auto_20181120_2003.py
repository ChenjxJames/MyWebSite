# Generated by Django 2.1.2 on 2018-11-20 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myUsers', '0002_auto_20181120_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uName',
            field=models.CharField(max_length=32, verbose_name='用户姓名'),
        ),
    ]