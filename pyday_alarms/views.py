from django.shortcuts import render
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect


class AlarmView(View):

    @method_decorator(login_required)
    def get(self, request):
        return HttpResponse(url)

    @method_decorator(login_required)
    def post(self, request):
        pass
