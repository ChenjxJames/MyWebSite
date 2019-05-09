# Generated by Django 2.1.2 on 2019-01-16 23:52

from django.db import migrations, models
import myCloud.models


class Migration(migrations.Migration):

    dependencies = [
        ('myCloud', '0010_auto_20181224_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileinfo',
            name='fExtension',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='文件后缀'),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='fFile',
            field=models.FileField(blank=True, null=True, upload_to=myCloud.models.FileInfo.user_directory_path, verbose_name='文件（路径）'),
        ),
    ]