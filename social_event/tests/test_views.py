import time, json
from django.test import TestCase

from social_event.models import *
from social_event.services import authentication

class TestView(TestCase):
    def setUp(self):
        current_time = int(time.time())
        user = User(username='user01', password="password")
        authentication.generate_token(user)
        user.save()
        channel = Channel(name='Channel 1')
        channel.save()
        event = Event(title="Science March",
            description="Science doesn't care what you believe.",
            start_time=current_time, end_time=current_time,
            channel=channel,
            location="White House",
            address="Washington DC",
            lat=100.1234, lon=100.1234,
            main_picture="http://social_events/images/00001.png"
        )
        event.save()
        event.create_comment(user=user, content="My comment 1")
        event.create_like(user=user)
        event.create_participant(user=user)
        # Comment(event=event, user=user, content="My comment 1").save()
        # Like(event=event, user=user).save()
        # Participant(event=event, user=user).save()
        channel2 = Channel(name='Channel 2')
        channel2.save()
        event2 = Event(title="Event 2",
            description="Event description",
            start_time=current_time, end_time=current_time,
            channel=channel2,
            location="Event location",
            address="Event address",
            lat=100.1234, lon=100.1234,
            main_picture="http://social_events/images/00001.png"
        )
        event2.save()

    def test_user_sign_in(self):
        url = '/api/users/sign_in'

        user = User(username='user01', password="password")
        user.save()

        response = self.client.post(url, data={ "username": user.username, "password": "wrong password" })
        self.assertEqual(response.status_code, 401)

        response = self.client.post(url, data={ "username": "wrong username", "password": "password" })
        self.assertEqual(response.status_code, 401)

        response = self.client.post(url, data={ "username": "user01", "password": "password" })
        self.assertEqual(response.status_code, 200)

    def test_channels(self):
        url = '/api/channels'
        token = User.objects.get(username='user01').token

        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        response = self.client.get(url, HTTP_AUTHORIZATION='Token wrong token')
        self.assertEqual(response.status_code, 401)

        response = self.client.get(url, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)

    def test_event(self):
        url = '/api/events/'
        token = User.objects.get(username='user01').token

        response = self.client.get(url + '0', HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url + str(Event.objects.first().id), HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)

    def test_events(self):
        url = '/api/events'
        token = User.objects.get(username='user01').token

        response = self.client.get(url, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 403)

        response = self.client.get(url, {"channel_id": Channel.objects.first().id, "ts": int(time.time()) }, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

        response = self.client.get(url, {"page": 2, "per": 1, "ts": int(time.time())}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)
        parsed_response = json.loads(response.content)
        self.assertEqual(len(parsed_response), 1)

    def test_comment_create(self):
        url = "/api/comments"
        token = User.objects.get(username='user01').token

        event = Event.objects.first()
        total_event_comment = event.total_comments

        response = self.client.post(url, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url, {"event_id": "0"}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 404)

        response = self.client.post(url, {"event_id": event.id}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url, {"event_id": event.id, "content": "New comment"}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Comment.objects.filter(content="New comment").first())
        self.assertEqual(Event.objects.get(pk=event.id).total_comments, total_event_comment + 1)


    def test_comments(self):
        url = "/api/comments"
        token = User.objects.get(username='user01').token

        event = Event.objects.first()
        response = self.client.get(url, {"event_id": event.id}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)
        parsed_response = json.loads(response.content)
        self.assertEqual(len(parsed_response), len(event.comment_set.all()))

    def test_like_delete(self):
        url = "/api/unlikes/"
        token = User.objects.get(username='user01').token

        like = Like.objects.first()
        total_like = len(Like.objects.all())
        total_event_like = like.event.total_likes

        response = self.client.post(url + "0", HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 404)

        response = self.client.post(url + str(like.id), HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Like.objects.all()), total_like - 1)
        self.assertEqual(Event.objects.get(pk=like.event.id).total_likes, total_event_like - 1)

    def test_like_create(self):
        url = "/api/likes"
        user = User(username='user03', password="password")
        authentication.generate_token(user)
        user.save()
        token = user.token
        total_like = len(Like.objects.all())
        event = Event.objects.first()
        total_event_like = event.total_likes

        response = self.client.post(url, {"event_id": event.id}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Like.objects.all()), total_like + 1)
        self.assertEqual(Event.objects.get(pk=event.id).total_likes, total_event_like + 1)

        response = self.client.post(url, {"event_id": event.id}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 400)

    def test_likes(self):
        url = "/api/likes"
        token = User.objects.get(username='user01').token
        event = Event.objects.first()

        response = self.client.get(url, {"event_id": event.id}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)

    def test_participant_delete(self):
        url = "/api/unparticipants/"
        token = User.objects.get(username='user01').token

        participant = Participant.objects.first()
        total_participant = len(Participant.objects.all())
        total_event_participant = participant.event.total_participants

        response = self.client.post(url + "0", HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 404)

        response = self.client.post(url + str(participant.id), HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Participant.objects.all()), total_participant - 1)
        self.assertEqual(Event.objects.get(pk=participant.event.id).total_participants, total_event_participant - 1)

    def test_participant_create(self):
        url = "/api/participants"
        user = User(username='user03', password="password")
        authentication.generate_token(user)
        user.save()
        token = user.token
        total_participant = len(Participant.objects.all())
        event = Event.objects.first()
        total_event_participant = event.total_participants

        response = self.client.post(url, {"event_id": event.id}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Participant.objects.all()), total_participant + 1)
        self.assertEqual(Event.objects.get(pk=event.id).total_participants, total_event_participant + 1)

        response = self.client.post(url, {"event_id": event.id}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 400)

    def test_participants(self):
        url = "/api/participants"
        token = User.objects.get(username='user01').token
        event = Event.objects.first()

        response = self.client.get(url, {"event_id": event.id}, HTTP_AUTHORIZATION="Token " + token)
        self.assertEqual(response.status_code, 200)
