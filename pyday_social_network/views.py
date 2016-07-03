from django.shortcuts import render
from django.http import HttpResponse
from pyday_social_network.forms import UploadPictureForm, LoginUserForm, UploadSongForm, RegisterUserForm
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
# from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from pyday_social_network.services import register_user_post, register_user_get, anonymous_required, make_song, make_picture, give_all_users, map_users_follows, return_user, post_redirect
from django.views.generic import View, FormView
from django.utils.decorators import method_decorator
from pyday.views import UploadView


class RegisterView(FormView):
    template_name = 'register_user.html'
    form_register_class = RegisterUserForm
    form_login_class = LoginUserForm
    success_url = '/register_success/'
    fail_url = '/register_fail/'

    @method_decorator(anonymous_required(redirect_to='/social/main'))
    def get(self, request):
        data_get = register_user_get(request, self.form_register_class, self.form_login_class)
        return render(request, 'register_user.html', data_get)

    @method_decorator(anonymous_required(redirect_to='/social/main'))
    def post(self, request):
        try:
            if register_user_post(request, self.form_register_class):
                return HttpResponse('стаа!')
            return HttpResponse('невалидна форма')
        except ValidationError:
            return HttpResponse('невалиден мейл, бре')


class UploadPictureView(UploadView):
    template_name = 'upload_picture.html'
    form_class = UploadPictureForm
    post_function = staticmethod(make_picture)
    success_url = '/social/main'


class UploadSongView(UploadView):
    template_name = 'upload_song.html'
    form_class = UploadSongForm
    post_function = staticmethod(make_song)
    success_url = '/social/main'


@post_redirect(redirect_to='/social/main')
@require_POST
def login_user(request):
    form = LoginUserForm(data=request.POST)

    if not form.is_valid():
        return HttpResponse('невалидна форма')

    form = form.cleaned_data
    user = authenticate(email=form['email'], password=form['password'])

    if user is None:
        return HttpResponse("Невалидни email и/или парола")

    if user.is_active:
        login(request, user)
        return HttpResponseRedirect('/social/main')
    else:
        return HttpResponse('активирайте акаунта си')


@login_required
def main(request):
    following = request.user.following
    followers = request.user.followers
    return render(request, 'main.html', {'user': request.user,
                                         'followers': followers, 'following': following})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponse('Youve logged out')


@login_required
def display_all_users(request):
    users = give_all_users()
    users_mapped = map_users_follows(request.user, users)
    return render(request, 'all_users.html', {'users': users_mapped})


@login_required
def display_following(request):
    users_mapped = map_users_follows(request.user, request.user.following)
    return render(request, 'all_users.html', {'users': users_mapped})


@login_required
def display_followers(request):
    users_mapped = map_users_follows(request.user, request.user.followers)
    return render(request, 'all_users.html', {'users': users_mapped})


@login_required
def display_friends(request):
    users_mapped = map_users_follows(request.user, request.user.friends)
    return render(request, 'all_users.html', {'users': users_mapped})


@login_required
def follow(request, user):
    success, user = request.user.follow(user)
    if not success:
        return HttpResponse('Youve already followed this user {}'.format(user.email))
    return HttpResponse('Youve followed {}'.format(user.email))


@login_required
def unfollow(request, user):
    success, user = request.user.unfollow(user)
    if not success:
        return HttpResponse('You dont follow this user {}'.format(user.email))
    return HttpResponse('Youve unfollowed {}'.format(user.email))


@login_required
def display_profile(request, user):
    user = return_user(user)
    following = request.user.following
    followers = request.user.followers
    return render(request, 'profile.html', {'user': user,
                  'followers': followers, 'following': following})
