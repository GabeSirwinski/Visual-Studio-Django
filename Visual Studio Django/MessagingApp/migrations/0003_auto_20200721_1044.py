# Generated by Django 2.2.14 on 2020-07-21 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MessagingApp', '0002_auto_20200719_2119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='chainId',
        ),
        migrations.RemoveField(
            model_name='message',
            name='subject',
        ),
    ]
