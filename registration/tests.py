from django.test import TestCase
from django.contrib.auth.models import User

from registration.models import BetaKey


class BetaKeyTests(TestCase):
    def test_create_keys(self):
        limit = 10
        key = BetaKey.objects.create_keys(limit)

        self.assertEquals(key.remaining, limit)
        self.assertSequenceEqual(key.created, [])
        self.assertEquals(len(key.key), 15)

    def test_valid_key_no_such_key_false(self):
        self.assertFalse(BetaKey.objects.valid_key('nosuchkey'))

    def test_valid_key_no_no_keys_remaining_false(self):
        key = BetaKey.objects.create_keys(0)
        self.assertFalse(BetaKey.objects.valid_key(key.key))

    def test_valid_key_no_no_keys_remaining_false(self):
        key = BetaKey.objects.create_keys(1)
        self.assertTrue(BetaKey.objects.valid_key(key.key))

    def test_keys_available_unlimited_is_true(self):
        key = BetaKey.objects.create_keys()
        self.assertTrue(key.keys_available())

    def test_no_keys_available_return_false(self):
        key = BetaKey.objects.create_keys(0)
        self.assertFalse(key.keys_available())

    def test_register_user(self):
        user = User.objects.create(username='test',
                                   email='test@rockt.ca')
        key = BetaKey.objects.create_keys(1)
        key.register_user(user)
        self.assertEquals(key.remaining, 0)
        self.assertIn('user', key.created[0])
        self.assertIn('id', key.created[0])
        self.assertEquals(key.created[0]['user'], user.username)
        self.assertEquals(key.created[0]['id'], user.id)

        key = BetaKey.objects.create_keys(-1)
        key.register_user(user)
        self.assertEquals(key.remaining, -1)
