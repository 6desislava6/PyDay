from pyday_social_network.models import PyDayUser


class PyDayUserAuth:

    def authenticate(self, email=None, password=None):
        try:
            user = PyDayUser.objects.get(email=email)
            if user.check_password(password):
                return user
            #return PyDayUser.objects.get(pk=1)
        except PyDayUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = PyDayUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except PyDayUser.DoesNotExist:
            return None
