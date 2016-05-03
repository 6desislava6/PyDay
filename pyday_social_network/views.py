from django.shortcuts import render
from django.http import HttpResponse
from pyday_social_network.forms import UploadPictureForm, LoginUserForm
from django.core.exceptions import ValidationError
from pyday_social_network.services import RegisterUserUtilities
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
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
    form = LoginUserForm(data=request.POST)
    # A  Form instance has an is_valid() method, which runs validation
    # routines for all its fields. When this method is called, if all fields
    # contain valid data, it will
    # place the form’s data in its cleaned_data attribute.
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse())
            else:
                return HttpResponse('активирайте акаунта си')
        else:
            return HttpResponse("Невалидни email и/или парола")
    return HttpResponse('невалидна форма')


def main(request):
    return render(request, 'main.html')
