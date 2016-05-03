from pyday_social_network.forms import RegisterUserForm, LoginUserForm
from pyday_social_network.models import PyDayUser


class RegisterUserUtilities:
    @staticmethod
    def register_user_post(request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            PyDayUser.objects.create_user_request(request)
            return True
        return False

    @staticmethod
    def register_user_get(request):
        return {'users': PyDayUser.objects.all(),
                'form_register': RegisterUserForm(),
                'form_login': LoginUserForm()}

