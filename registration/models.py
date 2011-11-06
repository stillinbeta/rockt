from hashlib import md5
from random import random

from django.db import models
from djangotoolbox.fields import ListField
from django.contrib.auth.models import User


class BetaKeyManager(models.Manager):
    def create_keys(self, limit=-1):
        key = md5(str(random()) + ' NaCl').hexdigest()[:15]
        return self.create(key=key, remaining=limit)

    def valid_key(self, key):
        try:
            return self.get(key=key).keys_available()
        except BetaKey.DoesNotExist:
            return False


class BetaKey(models.Model):
    key = models.CharField(max_length=15, unique=True)
    remaining = models.IntegerField()
    created = ListField()

    objects = BetaKeyManager()

    def keys_available(self):
        if self.remaining == -1:
            return True
        return self.remaining > 0

    def register_user(self, user):
        self.created.append({'user': user.username, 'id': user.id})
        if not self.remaining == -1:
            self.remaining -= 1
        self.save()


class WaitingList(models.Model):
    email = models.EmailField(unique=True)
    sent = models.BooleanField(default=False)
