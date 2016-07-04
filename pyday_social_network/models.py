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
        user.save()
        return user

# using=self._db

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

    def _follow_unfollow_inner(self, other, follow=True):
        other = PyDayUser.objects.get(pk=other)
        condition = self.follows(other.id) if follow else not self.follows(other)
        if condition:
            return False, other

        if follow:
            FollowingRelation(follower=self, followed=other).save()
        else:
            FollowingRelation.objects.get(follower=self,
                                          followed=other).delete()
        return True, other

    def follows(self, other):
        if FollowingRelation.objects.all().filter(follower=self,
                                                  followed=other):
            return True
        return False

    def follow(self, other):
        return self._follow_unfollow_inner(other)

    def unfollow(self, other):
        return self._follow_unfollow_inner(other, False)

    @property
    def followers(self):
        return [rel.follower for rel in FollowingRelation.objects.all().filter(followed=self)]

    @property
    def following(self):
        return [rel.followed for rel in FollowingRelation.objects.all().filter(follower=self)]

    @property
    def friends(self):
        return list(set(self.followers) & set(self.following))


class Song(models.Model):
    owner = models.ForeignKey('PyDayUser', on_delete=models.CASCADE)
    song = models.FileField(upload_to='songs/')


class FollowingRelation(models.Model):
    follower = models.ForeignKey(
        'PyDayUser', on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(
        'PyDayUser', on_delete=models.CASCADE, related_name='followed')
