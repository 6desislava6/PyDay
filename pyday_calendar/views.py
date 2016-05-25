from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from pyday_calendar.forms import CreateEventForm


def index(request):
    return HttpResponse("")


@login_required
def create_event(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            return HttpResponse(str(request))
        else:
            return HttpResponse('не стаа')
    else:
        form = CreateEventForm()
        return render(request, 'create_event.html', {'form': form})


#TODO
# https://docs.djangoproject.com/en/1.9/topics/class-based-views/intro/
