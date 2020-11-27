from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

class User(AbstractUser):

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    email = models.EmailField(_('email address'), max_length=255, db_index=True, unique=True,
        error_messages={
            'unique': _("This email has already registered. Choose another one, please"),
        })
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        null=True,
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
