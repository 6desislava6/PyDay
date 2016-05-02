from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now


class PyDayManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('No email!')

        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save()

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class PyDayUser(AbstractBaseUser):
    email = models.CharField(max_length=200, unique=True, default='')
    # password = models.CharField(max_length=200, default='')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    picture = models.FileField(upload_to='pictures/')
    date_joined = models.DateTimeField(default=now())
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = PyDayManager()


'''
class PyDayUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.FileField(upload_to='pictures/')
    objects = UserManager()'''
