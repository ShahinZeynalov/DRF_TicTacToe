from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['',]

    email = models.EmailField(_('email address'), max_length=255, db_index=True, unique=True,
        error_messages={
            'unique': _("This email has already registered. Choose another one, please"),
        })
