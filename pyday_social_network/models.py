from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now
from django.core.validators import validate_email
from pyday.settings import GENERIC_PROFILE_PIC


class PyDayManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name,
                     is_staff=False, is_active=True, is_superuser=False,
                     **extra_fields):
        if not email:
            raise ValueError('No email!')

        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff,
                          is_active=is_active, password=password,
                          first_name=first_name, last_name=last_name,
                          **extra_fields)
        user.set_password(password)
        user.clean_fields()
        user.save(using=self._db)
        return user

    def create_user_request(self, request):
        self._create_user(email=request.POST['email'],
                          password=request.POST['password'],
                          first_name=request.POST['first_name'],
                          last_name=request.POST['last_name'])


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
