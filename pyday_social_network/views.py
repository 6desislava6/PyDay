from django.shortcuts import render
from django.http import HttpResponseRedirect
from pyday_social_network.forms import UploadPictureForm


def upload_picture(request):
    if request.method == 'POST':
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadPictureForm()
    return render(request, 'upload_picture.html', {'form': form})
