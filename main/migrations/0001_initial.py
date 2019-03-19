# Generated by Django 2.1.5 on 2019-03-15 16:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.IntegerField()),
                ('update_time', models.DateTimeField(default=datetime.datetime.now)),
                ('call_date', models.DateField(default=datetime.date.today)),
                ('call_last', models.FloatField()),
                ('call_chg', models.FloatField()),
                ('call_bid', models.FloatField()),
                ('call_ask', models.FloatField()),
                ('call_vol', models.IntegerField()),
                ('call_open_int', models.IntegerField()),
                ('root', models.CharField(max_length=10)),
                ('strike', models.FloatField()),
                ('put_date', models.DateField(default=datetime.date.today)),
                ('put_last', models.FloatField()),
                ('put_chg', models.FloatField()),
                ('put_bid', models.FloatField()),
                ('put_ask', models.FloatField()),
                ('put_vol', models.IntegerField()),
                ('put_open_int', models.IntegerField()),
            ],
        ),
    ]