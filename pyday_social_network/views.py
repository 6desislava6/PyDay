from django.shortcuts import render
from django.http import HttpResponse
from pyday_social_network.forms import UploadPictureForm
from django.core.exceptions import ValidationError
from pyday_social_network.services import RegisterUserUtilities
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.contrib import auth


def upload_picture(request):
    if request.method == 'POST':
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            # update user info
            return HttpResponse('стаа!')
        else:
            return HttpResponse('не стаа')
    else:
        form = UploadPictureForm()
        return render(request, 'upload_picture.html', {'form': form})


# reverse връща от името на url самия url
def register_login_user(request):
    if request.method == 'POST':
        try:
            if RegisterUserUtilities.register_user_post(request):
                return HttpResponse('стаа!')
            return HttpResponse('невалидна форма')
        except ValidationError:
            return HttpResponse('невалиден мейл, бре')
    else:
        data_get = RegisterUserUtilities.register_user_get(request)
        return render(request, 'register_user.html', data_get)


@require_POST
def login_user(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/main')
        else:
            return HttpResponse('disabled account')
    else:
        return HttpResponse(password)


def main(request):
    return render(request, 'main.html')
