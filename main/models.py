from django.db import models
from datetime import date
from datetime import datetime
# Create your models here.
class Chain(models.Model):
    record_id = models.IntegerField()
    record_date = models.DateField(default=date.today)
    call_date = models.DateField(default=date.today)
    call_last = models.FloatField()
    call_chg = models.FloatField()
    call_bid = models.FloatField()
    call_ask = models.FloatField()
    call_vol = models.IntegerField()
    call_open_int = models.IntegerField()
    root = models.CharField(max_length = 10)
    strike = models.FloatField()
    put_date = models.DateField(default=date.today)
    put_last = models.FloatField()
    put_chg = models.FloatField()
    put_bid = models.FloatField()
    put_ask = models.FloatField()
    put_vol = models.IntegerField()
    put_open_int = models.IntegerField()

