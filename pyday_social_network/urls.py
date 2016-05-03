from django.conf.urls import url
from django.conf.urls import patterns

from pyday_social_network import views

app_name = 'pyday_social_network'
urlpatterns = [
    url(r'^upload_picture/$', views.upload_picture, name='upload_picture'),
    url(r'^register/$', views.register_login_user, name='register_login'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^main/$', views.main, name='main'),

]

urlpatterns += patterns('pyday_social_network.views',
                        url(r'^list/$', 'list', name='list'))
