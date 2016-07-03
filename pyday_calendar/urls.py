from django.conf.urls import url
from django.conf.urls import patterns
from pyday_calendar import views

app_name = 'pyday_calendar'
urlpatterns = [
    url(r'^create_event/$', views.CreateEventView.as_view(), name='create-event'),
    url(r'^daily_events/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})$', views.DailyEventView.as_view(), name='daily-events'),
    url(r'monthly_events/$', views.MontlyEventView.as_view(), name='monthly-events'),

]

urlpatterns += patterns('pyday_social_network.views',
                        url(r'^list/$', 'list', name='list'))
