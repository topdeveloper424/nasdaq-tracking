from django.urls import path,include
from . import views

app_name = 'main'


urlpatterns = [
    path('', views.index,name='index'),
    path('get-data', views.get_data,name='get_data'),
    path('chart', views.chart,name='chart'),
    path('get-chart-data', views.get_chart_data,name='get_chart_data'),
]
