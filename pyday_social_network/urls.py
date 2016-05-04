from django.conf.urls import url
from django.conf.urls import patterns

from pyday_social_network import views

app_name = 'pyday_social_network'
urlpatterns = [
    url(r'^upload_picture/$', views.upload_picture, name='upload_picture'),
    url(r'^upload_song/$', views.upload_song, name='upload_song'),
    url(r'^register/$', views.register_login_user, name='register-login'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^main/$', views.main, name='main'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^all/$', views.display_all_users, name='all_users'),
    url(r'^following/$', views.display_following, name='following'),
    url(r'^followers/$', views.display_followers, name='followers'),
    url(r'^friends/$', views.display_friends, name='friends'),
    url(r'^follow/(?P<user>[0-9]+)$', views.follow, name='follow'),
    url(r'^unfollow/(?P<user>[0-9]+)$', views.unfollow, name='unfollow'),
    url(r'^profile/(?P<user>[0-9]+)$', views.display_profile, name='profile'),
]

urlpatterns += patterns('pyday_social_network.views',
                        url(r'^list/$', 'list', name='list'))

# handler404 = 'pyday.views.404'
