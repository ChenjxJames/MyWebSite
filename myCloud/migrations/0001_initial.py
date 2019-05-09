# Generated by Django 2.1.2 on 2018-11-20 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileInfo',
            fields=[
                ('fId', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='文件编号')),
                ('fName', models.CharField(max_length=255, verbose_name='文件名')),
                ('fFloderId', models.CharField(max_length=10, verbose_name='文件所在父文件夹编号')),
                ('fIsFloder', models.BooleanField(verbose_name='是否为文件夹')),
                ('fUploadTime', models.DateTimeField(verbose_name='文件上传时间')),
                ('fUserId', models.CharField(max_length=10, verbose_name='文件所属的用户编号')),
            ],
        ),
    ]