from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    def _create_user(self,
                     email,
                     password=None,
                     is_merchant=False,
                     is_staff=False,
                     is_superuser=False):
        """ Creates and saves new user with email and password"""
        now = datetime.now()

        if not email:
            raise ValueError("An email address is required to login")
        if not password:
            raise ValueError("An password is required to login")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_merchant=is_merchant,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None):
        return self._create_user(email, password, False, False, False)

    def create_superuser(self, email, password=None):
        return self._create_user(email, password, True, True, True)


class CustomUser(AbstractBaseUser):
    email = models.EmailField(_('Email Address'), unique=True)
    first_name = models.CharField(_('First Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30, blank=True)
    area_code = models.CharField(_('Area Code'), max_length=30, blank=True)
    country_code = models.CharField(
        _('Country Code'), max_length=30, blank=True)

    is_active = models.BooleanField(default=True)
    is_merchant = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        fullname = "%s %s" % (self.first_name, self.last_name)
        return fullname.strip()

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
