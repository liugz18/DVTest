# Generated by Django 3.2.12 on 2022-02-27 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Run', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='run',
            name='imgpath',
        ),
        migrations.AddField(
            model_name='run',
            name='finishdate',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='run',
            name='key',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='run',
            name='startdate',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='run',
            name='user',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='run',
            name='where',
            field=models.CharField(default='', max_length=100),
        ),
    ]
