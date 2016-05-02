from django.shortcuts import render
from django.http import HttpResponse
from pyday_social_network.forms import UploadPictureForm
from pyday_social_network.models import PyDayUser
from django.core.exceptions import ValidationError
# from django.http import HttpResponseRedirect


def upload_picture(request):
    if request.method == 'POST':
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                PyDayUser.objects.create_user_request(request)
            except ValidationError:
                return HttpResponse('невалиден мейл, бре')
            else:
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
