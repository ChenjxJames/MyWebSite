# Generated by Django 2.1.2 on 2018-12-24 22:48

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myCloud', '0007_auto_20181224_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='fFile',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='D:\\MyWebSite\\MyWebSite\\MyWebSite\\upload'), upload_to='cloud_files/%Y/%m/%d/%H/%M/%S/', verbose_name='文件（路径）'),
        ),
    ]
