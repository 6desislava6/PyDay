from django.shortcuts import render
from django.http import HttpResponse
from pyday_social_network.forms import UploadPictureForm, LoginUserForm, UploadSongForm
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
# from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from pyday_social_network.services import register_user_post, register_user_get, anonymous_required, make_song, give_all_users, map_users_follows, return_user
from django.views.generic import View
from django.utils.decorators import method_decorator


@anonymous_required(redirect_to='/social/main')
def register_login_user(request):
    if request.method == 'POST':
        try:
            if register_user_post(request):
                return HttpResponse('стаа!')
            return HttpResponse('невалидна форма')
        except ValidationError:
            return HttpResponse('невалиден мейл, бре')
    else:
        data_get = register_user_get(request)
        return render(request, 'register_user.html', data_get)


class UploadView(View):
    template_name = 'form_template.html'

    @method_decorator(login_required)
    def get(self, request):
        form = UploadPictureForm()
        return render(request, 'upload_picture.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.picture = form.cleaned_data['picture']
            request.user.save()
            return HttpResponse('стаа!')
        else:
            return HttpResponse('не стаа')


@login_required
def upload_song(request):
    if request.method == 'POST':
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            make_song(request.user, form)
            return HttpResponse('стаа!')
        else:
            return HttpResponse('не стаа')
    else:
        form = UploadSongForm()
        return render(request, 'upload_song.html', {'form': form})


@require_POST
def login_user(request):
    form = LoginUserForm(data=request.POST)

    if form.is_valid():
        form = form.cleaned_data
        user = authenticate(email=form['email'], password=form['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/social/main')
            else:
                return HttpResponse('активирайте акаунта си')
        else:
            return HttpResponse("Невалидни email и/или парола")
    return HttpResponse('невалидна форма')


@login_required
def main(request):
    following = request.user.following
    followers = request.user.followers
    return render(request, 'main.html', {'user': request.user, 'followers': followers, 'following': following})


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
    return render(request, 'profile.html', {'user': user, 'followers': followers, 'following': following})
