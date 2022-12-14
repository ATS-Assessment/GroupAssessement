from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address.')

        if not username:
            raise ValueError('User must have an email address.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
        )

        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    image = models.ImageField(default='media/default.png', upload_to='media/')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser



