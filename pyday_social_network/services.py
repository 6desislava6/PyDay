from pyday_social_network.forms import RegisterUserForm, LoginUserForm
from pyday_social_network.models import PyDayUser, Song
from django.http import HttpResponseRedirect


def register_user_post(request):
    form = RegisterUserForm(request.POST)
    if form.is_valid():
        PyDayUser.objects.create_user_request(request)
        return True
    return False


def register_user_get(request):
    return {'users': PyDayUser.objects.all(),
            'form_register': RegisterUserForm(),
            'form_login': LoginUserForm()}


def make_song(user, form):
    Song(owner=user, song=form.cleaned_data['song']).save()


def give_all_users():
    return PyDayUser.objects.all


def anonymous_required(redirect_to=None):
    def inner_decorator(func):
        def decorated(request, *args, **kwargs):
            if request.user is not None and request.user.is_authenticated():
                return HttpResponseRedirect(redirect_to)
            return func(request, *args, **kwargs)
        return decorated
    return inner_decorator
