# Generated by Django 3.2.12 on 2022-02-27 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Run', '0001_initial'),
        ('Album', '0002_alter_album_run'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='run',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Run.run'),
        ),
    ]
