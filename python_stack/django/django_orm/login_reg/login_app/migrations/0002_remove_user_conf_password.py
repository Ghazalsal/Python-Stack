# Generated by Django 2.2.4 on 2021-05-27 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='conf_password',
        ),
    ]