from django.shortcuts import render
from django.http import HttpResponse
from pyday_social_network.forms import UploadPictureForm
from pyday_social_network.models import PyDayUser
# from django.http import HttpResponseRedirect


def upload_picture(request):
    if request.method == 'POST':
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            PyDayUser.objects.create_user(first_name=request.POST['first_name'],
                                  last_name=request.POST['last_name'],
                                  email=request.POST['email'],
                                  picture=request.FILES['file'])
            return HttpResponse('стаа!')

        else:
            return HttpResponse('не стаа')
    else:
        form = UploadPictureForm()

    users = PyDayUser.objects.all()
    return render(
        request,
        'upload_picture.html',
        {'users': users, 'form': form},
    )
