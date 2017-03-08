from django.test import TestCase

from social_event.models import *

class TestUser(TestCase):

    def test_generate_password_digest(self):
        user = User(username="user01", password="password")
        user.save()
        self.assertIsNotNone(user.password_digest)
        self.assertIsNotNone(user.salt)
