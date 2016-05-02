from django.conf.urls import url
from django.conf.urls import patterns

from . import views

app_name = 'pyday_social_network'
urlpatterns = [
    url(r'^upload_picture/$', views.upload_picture, name='index'),
]

urlpatterns += patterns('pyday_social_network.views',
                        url(r'^list/$', 'list', name='list'),
                        )
