from django.conf.urls import url
from django.conf.urls import patterns
from pyday_alarms import views

app_name = 'pyday_alarms'
urlpatterns = [
    url(r'^alarms/$', views.AlarmView.as_view(), name='create-event'),
]

'''urlpatterns += patterns('pyday_social_network.views',
                        url(r'^list/$', 'list', name='list'))
'''
