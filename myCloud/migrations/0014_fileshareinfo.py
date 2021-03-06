# Generated by Django 2.1.2 on 2019-05-14 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myCloud', '0013_fileinfo_fmd5'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileShareInfo',
            fields=[
                ('fShareId', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='文件分享编号')),
                ('fId', models.CharField(max_length=10, verbose_name='文件编号')),
                ('fKey', models.CharField(max_length=32, verbose_name='访问密钥')),
                ('fTimestamp', models.DateTimeField(auto_now_add=True, verbose_name='分享创建时间戳')),
                ('fDeadline', models.DateTimeField(verbose_name='分享截止时间')),
            ],
        ),
    ]
