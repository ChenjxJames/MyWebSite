# Generated by Django 2.1.2 on 2018-11-20 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myUsers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='uEamil',
            new_name='uEmail',
        ),
    ]
