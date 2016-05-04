from django.conf.urls import url
from django.conf.urls import patterns
from . import views

app_name = 'pyday_calendar'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_event/$', views.create_event, name='create-event'),
]

urlpatterns += patterns('pyday_social_network.views',
                        url(r'^list/$', 'list', name='list'))
