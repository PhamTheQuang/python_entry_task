import time, json
from django.test import TestCase

from social_event.models import *
from social_event.services import authentication

class TestView(TestCase):
    def setUp(self):
        current_time = int(time.time())
        self.admin = Admin(username='admin01', password="password")
        self.admin.generate_token
        self.admin.save()

    def test_user_sign_in(self):
        url = "/admin/sign_in"

        response = self.client.post(url, data={"username": self.admin.username, "password": "wrong password"})
        self.assertContains(response, "Incorrect combination of username and password.")

        response = self.client.post(url, data={"username": self.admin.username, "password": "password"})
        self.assertRedirects(response, "/admin/events")
