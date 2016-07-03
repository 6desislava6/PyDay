from pyday_social_network.models import PyDayUser, Song
from django.http import HttpResponseRedirect


def register_user_post(request, form_register_class):
    form = form_register_class(request.POST)
    if form.is_valid():
        PyDayUser.objects.create_user_request(request)
        return True
    return False
    # да хващам exception-ите и да ги записвам в лог


def register_user_get(request, form_register_class, form_login_class):
    return {'users': PyDayUser.objects.all(),
            'form_register': form_register_class(),
            'form_login': form_login_class()}


def make_song(user, form):
    Song(owner=user, song=form.cleaned_data['song']).save()


def make_picture(user, form):
    user.picture = form.cleaned_data['picture']
    user.save()


def give_all_users():
    return list(PyDayUser.objects.all())


def map_users_follows(main_user, users):
    return [(user, main_user.follows(user.id)) for user in users]


def return_user(id):
    return PyDayUser.objects.get(pk=id)


def anonymous_required(redirect_to=None):
    def inner_decorator(func):
        def decorated(request, *args, **kwargs):
            if request.user is not None and request.user.is_authenticated():
                return HttpResponseRedirect(redirect_to)
            return func(request, *args, **kwargs)
        return decorated
    return inner_decorator


# I don't remember this one :D
def mapped_user(attribute):
    def mapper_users(func):
        def decorated(request, *args):
            user = request.user
            users = getattr(user, attribute)
            func


def post_redirect(redirect_to=None):
    def inner_decorator(func):
        def decorated(request, *args, **kwargs):
            if request.method != 'POST':
                return HttpResponseRedirect(redirect_to)
            return func(request, *args, **kwargs)
        return decorated
    return inner_decorator
