from __future__ import unicode_literals

from django.db import models
from django.db.models import constraints
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


import logging

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('email is missing')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    pass


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('registered'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    list_display = ('email',)
    ordering = ('email',)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    pass


class Visitor(models.Model):
    name = models.CharField(max_length=50)
    birth_date = models.DateField()
    passport_number = models.CharField(max_length=9)

    def __str__(self):
        return self.name

    pass


class Registration(models.Model):
    lend_date = models.DateField()
    return_date = models.DateField()
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)

    def __str__(self):
        r_str = '№ ' + str(self.id) + ', Name: ' + str(self.visitor) + ', Books: '
        for b in self.bookinstance_set.all():
            r_str += str(b)
        return r_str

    pass


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) + ', ' + str(self.author)

    pass


class BookInstance(models.Model):
    type = models.ForeignKey(Book, on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [
            constraints.UniqueConstraint(fields=['type', 'registration'], name='unique_booking')
        ]
        pass

    def __str__(self):
        return str(self.type) + ' № ' + str(self.id)

    pass
