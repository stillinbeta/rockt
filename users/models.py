from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import EmbeddedModelField,ListField

# Create your models here.

decimal_config = {'decimal_places':2,'max_digits':10}


class UserProfile(models.Model):
    balance = models.IntegerField()
    user = models.ForeignKey(User, unique=True)
    class InsufficientFundsException(Exception):
        pass
