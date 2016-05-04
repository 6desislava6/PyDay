from django.conf.urls import url
from . import views

app_name = 'pyday_calendar'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_event/$', views.create_event, name='create-event'),
]
