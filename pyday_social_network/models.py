from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now
from django.core.validators import validate_email
from pyday.settings import GENERIC_PROFILE_PIC


class PyDayManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('No email!')

        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.set_password(password)
        user.clean_fields()
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_user_request(self, request):
        self.create_user(first_name=request.POST['first_name'],
                         last_name=request.POST['last_name'],
                         email=request.POST['email'])


class PyDayUser(AbstractBaseUser):
    email = models.EmailField(max_length=200, unique=True, default='',
                              validators=[validate_email])
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    picture = models.FileField(upload_to='pictures/',
                               default=GENERIC_PROFILE_PIC)
    date_joined = models.DateTimeField(default=now())
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = PyDayManager()
