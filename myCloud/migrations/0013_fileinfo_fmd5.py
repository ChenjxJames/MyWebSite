# Generated by Django 2.1.2 on 2019-01-24 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myCloud', '0012_filetypeinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileinfo',
            name='fmd5',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='文件md5码'),
        ),
    ]
