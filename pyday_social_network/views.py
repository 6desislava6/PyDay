from django.shortcuts import render
from django.http import HttpResponse
from pyday_social_network.forms import UploadPictureForm, LoginUserForm, UploadSongForm, RegisterUserForm
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
# from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from pyday_social_network.services import *
from django.views.generic import View, FormView
from django.utils.decorators import method_decorator
from pyday.views import UploadView
from pyday_social_network.models import PyDayUser
from datetime import datetime
from pyday_calendar.forms import CreateEventForm
from pyday_alarms.forms import CreateAlarmForm
from random import randrange


class RegisterView(FormView):
    template_name = 'register_user.html'
    form_register_class = RegisterUserForm
    form_login_class = LoginUserForm
    success_url = '/register_success/'
    fail_url = '/register_fail/'

    @method_decorator(anonymous_required(redirect_to='/social/main'))
    def get(self, request):
        data_get = register_user_get(request, self.form_register_class,
                                     self.form_login_class)
        data_get['user'] = request.user
        return render(request, 'register_user.html', data_get)

    @method_decorator(anonymous_required(redirect_to='/social/main'))
    def post(self, request):
        if register_user_post(request, self.form_register_class):
            return render(request, 'error.html',
                          {'error': 'You have registered'})
        return render(request, 'error.html', {'error': 'Invalid form'})


class UploadPictureView(UploadView):
    # template_name = 'upload_picture.html'
    form_class = UploadPictureForm
    post_function = staticmethod(make_picture)
    success_url = '/social/main'


class UploadSongView(UploadView):
    # template_name = 'upload_song.html'
    form_class = UploadSongForm
    post_function = staticmethod(make_song)
    success_url = '/social/main'


@post_redirect(redirect_to='/social/main')
@anonymous_required(redirect_to='/social/main')
@require_POST
def login_user(request):
    form = LoginUserForm(data=request.POST)

    if not form.is_valid():
        return render(request, 'error.html', {'error': 'Invalid form'})

    form = form.cleaned_data
    user = authenticate(email=form['email'], password=form['password'])

    if user is None:
        return render(request, 'error.html',
                      {'error': 'Invalid email/password'})

    login(request, user)
    return HttpResponseRedirect('/social/main')


@login_required
def main(request):
    current_date = datetime.now()
    form = CreateEventForm(initial={'date': current_date})
    greeting = get_greeting(current_date.hour)
    current_events = get_current_events(current_date.hour, current_date,
                                        request.user)
    pic = randrange(1, 7)
    form_alarm = CreateAlarmForm()

    return render(request, 'main.html', {'user_request': request.user,
                                         **locals()})


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'error.html', {'error': "You have logged out"})


@login_required
def display_all_users(request):
    users = give_all_users()
    users_mapped = map_users_follows(request.user, users)
    return render(request, 'all_users.html',
                  {'users': users_mapped, 'user_request': request.user})


@login_required
def display_following(request):
    users_mapped = map_users_follows(request.user, request.user.following)
    return render(request, 'all_users.html',
                  {'users': users_mapped, 'user_request': request.user})


@login_required
def display_followers(request):
    users_mapped = map_users_follows(request.user, request.user.followers)
    return render(request, 'all_users.html',
                  {'users': users_mapped, 'user_request': request.user})


@login_required
def display_friends(request):
    users_mapped = map_users_follows(request.user, request.user.friends)
    return render(request, 'all_users.html',
                  {'users': users_mapped, 'user_request': request.user})


@login_required
def follow(request, user):
    success, user = request.user.follow(user)
    if not success:
        return render(request, 'error.html',
                      {'error': "You have already followed this user {}".format(user.email)})
    return HttpResponseRedirect('/social/profile')


@login_required
def unfollow(request, user):
    success, user = request.user.unfollow(user)
    if not success:
        return render(request, 'error.html',
                      {'error': "You do not follow this user {}".format(user.email)})
    return HttpResponseRedirect('/social/profile')


@login_required
def display_profile(request, user=None):
    try:
        user = return_user(user) if user else request.user
    except PyDayUser.DoesNotExist:
        return render(request, 'error.html', {'error': 'User does not exist.'})
    else:
        following = request.user.following
        followers = request.user.followers
        to_follow_button = user != request.user
        is_following = request.user.follows(user)
        form = UploadPictureForm()
        return render(request, 'profile.html', {'user_request': request.user,
                                                **locals()})


@login_required
@require_POST
def search_user(request):
    users_mapped = map_users_follows(request.user,
                                     search_users(request.POST["searched"]))
    return render(request, 'all_users.html',
                  {'users': users_mapped, 'user_request': request.user})
