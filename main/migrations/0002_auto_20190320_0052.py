# Generated by Django 2.1.5 on 2019-03-19 16:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chain',
            name='update_time',
        ),
        migrations.AddField(
            model_name='chain',
            name='record_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
