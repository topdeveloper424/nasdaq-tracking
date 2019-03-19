from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Max
from main.models import Chain
from django.views.decorators.csrf import csrf_exempt
import time 
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from datetime import date
import webbrowser
import threading
import json

def scrape():
    while True:
        url = "https://www.nasdaq.com/symbol/ndaq/option-chain?money=all"
        cur_time = datetime.now()
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        OptionsChain = soup.findAll('div',{'class':'OptionsChain-chart'})[0]
        #tbody = OptionsChain.findAll('tr')
        cur_date = date(cur_time.year,cur_time.month,cur_time.day)
        Chain.objects.filter(record_date=cur_date).delete()
        max_record = Chain.objects.all().aggregate(Max('record_id'))
        print(max_record)
        max_id = 0
        if max_record['record_id__max'] != None:
            max_id = max_record['record_id__max'] + 1
        trs = OptionsChain.findAll('tr')
        for tr in trs:
            tds = tr.findAll('td')
            if len(tds) < 5:
                continue
            call_date_txt = tds[0].text
            call_date_txt = call_date_txt.strip()
            call_date_txt = call_date_txt.replace(",","")
            call_date = datetime.strptime(call_date_txt, '%b %d %Y')

            call_last_txt = tds[1].text
            call_last_txt = call_last_txt.strip()
            call_last = 0
            try:
                call_last = float(call_last_txt)
            except Exception:
                pass

            call_chg_txt = tds[2].text
            call_chg_txt = call_chg_txt.strip()
            call_chg = 0
            try:
                call_chg = float(call_chg_txt)
            except Exception:
                pass

                        
            call_bid_txt = tds[3].text
            call_bid_txt = call_bid_txt.strip()
            call_bid = 0
            try:
                call_bid = float(call_bid_txt)
            except Exception:
                pass
            
            call_ask_txt = tds[4].text
            call_ask_txt = call_ask_txt.strip()
            call_ask = 0
            try:
                call_ask = float(call_ask_txt)
            except Exception:
                pass
            

            call_vol_txt = tds[5].text
            call_vol_txt = call_vol_txt.strip()
            call_vol = 0
            try:
                call_vol = int(call_vol_txt)
            except Exception:
                pass

            call_openint_txt = tds[6].text
            call_openint_txt = call_openint_txt.strip()
            call_openint = 0
            try:
                call_openint = int(call_openint_txt)
            except Exception:
                pass

            root = tds[7].text
            root = root.strip()


            strike_txt = tds[8].text
            strike_txt = strike_txt.strip()
            strike = 0
            try:
                strike = float(strike_txt)
            except Exception:
                pass
            

            put_date_txt = tds[9].text
            put_date_txt = put_date_txt.strip()
            put_date_txt = put_date_txt.replace(",","")
            put_date = datetime.strptime(put_date_txt, '%b %d %Y')

            put_last_txt = tds[10].text
            put_last_txt = put_last_txt.strip()
            put_last = 0
            try:
                put_last = float(put_last_txt)
            except Exception:
                pass


            put_chg_txt = tds[11].text
            put_chg_txt = put_chg_txt.strip()
            put_chg = 0
            try:
                put_chg = float(put_chg_txt)
            except Exception:
                pass
            
            put_bid_txt = tds[12].text
            put_bid_txt = put_bid_txt.strip()
            put_bid = 0
            try:
                put_bid = float(put_bid_txt)
            except Exception:
                pass

            put_ask_txt = tds[13].text
            put_ask_txt = put_ask_txt.strip()
            put_ask = 0
            try:
                put_ask = float(put_ask_txt)
            except Exception:
                pass

            put_vol_txt = tds[14].text
            put_vol_txt = put_vol_txt.strip()
            put_vol = 0
            try:
                put_vol = int(put_vol_txt)
            except Exception:
                pass
            

            put_openint_txt = tds[15].text
            put_openint_txt.strip()
            put_openint = 0
            try:
                put_openint = int(put_openint_txt)
            except Exception:
                pass
            chain = Chain(record_id=max_id, record_date=cur_date, call_date=call_date,call_last=call_last,call_chg=call_chg,call_bid=call_bid,call_ask=call_ask,call_vol=call_vol,call_open_int=call_openint,root=root,strike=strike,put_date=put_date,put_last=put_last,put_chg=put_chg,put_bid=put_bid,put_ask=put_ask,put_vol=put_vol,put_open_int=put_openint)
            chain.save()
        time.sleep(7200)


def start_timer():
    t = threading.Thread(target=scrape)
    t.start()


#webbrowser.open('http://127.0.0.1:8000/', new=2)
start_timer()

def index(request):
    record_ids = Chain.objects.values('record_id').distinct().all().order_by("-record_id")
    items = []
    print(record_ids)
    for record_id in record_ids:
        item = {}
        records = Chain.objects.filter(record_id=record_id['record_id'])
        item['record_id'] = record_id['record_id']
        item['update_time'] = records[0].record_date
        items.append(item)

    return render(request, 'table.html',{'updated_times':items})

def get_data(request):
    record_id = request.GET['record_id']
    if record_id == "":
        return HttpResponse(json.dumps(""),content_type="application/json")
    print(record_id)

    records = Chain.objects.filter(record_id=record_id)
    if len(records) > 0:
        serialized_queryset = serializers.serialize('json', records)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

def get_chart_data(request):
    chart_num = int(request.GET['chartSelect'])
    if chart_num == "":
        return HttpResponse(json.dumps(""),content_type="application/json")
    print(chart_num)
    today_time =  datetime.now()
    point_time = datetime.now()
    if chart_num == 0:
        point_time =  datetime.now()-timedelta(days=7)
    elif chart_num == 1:
        point_time =  monthdelta(point_time,-1)
    elif chart_num == 2:
        point_time =  monthdelta(point_time,-6)
    elif chart_num == 3:
        point_time =  monthdelta(point_time,-12)
    print(today_time)
    print(point_time)
    point_date = date(point_time.year,point_time.month,point_time.day)

    record_ids = Chain.objects.values('record_id').distinct().all().order_by("-record_id")
    items = []
    for record_id in record_ids:
        item = {}
        records = Chain.objects.filter(record_id=record_id['record_id'])
        item['record_id'] = record_id['record_id']
        item['update_time'] = records[0].record_date
        items.append(item)
    filters = []
    for item in items:
        print(point_date)

        if item['update_time'] >= point_date:
            filter_item = {}
            filter_item['record_id'] = item['record_id']
            filter_item['update_time'] = item['update_time'].strftime('%Y-%m-%d')
            data = Chain.objects.filter(record_id = item['record_id']).all()
            serialized_queryset = serializers.serialize('json', data)
            filter_item['data'] = serialized_queryset
            filters.append(filter_item)
    if len(filters) > 0:
        return HttpResponse(json.dumps(filters),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")


def chart(request):

    return render(request, 'chart.html')






