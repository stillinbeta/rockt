from base64 import b64encode

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class ApiTests(TestCase):
    def setUp(self):
        username = 'apitest'
        password = 'secret'

        self.user = User.objects.create(username=username,
                         email='joe@bloggs.com')
        self.user.set_password(password)
        self.user.save()

        self.auth_string = 'Basic ' + b64encode('{}:{}'.format(username,
                                                             'secret'))

    def _make_get(self, args=()):
        return self.client.get(reverse(self.api_name, args=args),
                               HTTP_AUTHORIZATION=self.auth_string)

    def _make_post(self, args=(), data={}):
        return self.client.post(reverse(self.api_name, args=args),
                                data={},
                                HTTP_AUTHORIZATION=self.auth_string)

    def assertStatusCode(self, response, code):
        self.assertEquals(response.status_code, code, 'Unexpected status code')

    def tearDown(self):
        self.user.delete()
