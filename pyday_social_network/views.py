from django.shortcuts import render
from django.http import HttpResponse
from pyday_social_network.forms import UploadPictureForm, LoginUserForm, UploadSongForm
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
# from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from pyday_social_network.services import register_user_post, register_user_get, anonymous_required, make_song, give_all_users


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


@login_required
def upload_picture(request):
    if request.method == 'POST':
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.picture = form.cleaned_data['picture']
            request.user.save()
            return HttpResponse('стаа!')
        else:
            return HttpResponse('не стаа')
    else:
        form = UploadPictureForm()
        return render(request, 'upload_picture.html', {'form': form})


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
    return render(request, 'main.html', {'user': request.user})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponse('Youve logged out')


def display_all_users(request):
    return render(request, 'all_users.html', {'users': give_all_users()})
