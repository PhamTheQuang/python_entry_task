import time, random;

from django.core.management.base import BaseCommand
from django.db import transaction
from social_event.models import *

BLOCK_SIZE = 10000

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        current_time = int(time.time())
        admin = Admin(username='admin01', password="password")
        admin.generate_token
        admin.save()

        channel_count = 10
        user_count = 1000000
        event_count = 1000000
        comment_count = 1

        channels = []
        with transaction.atomic():
            for i in range(channel_count):
                channel = Channel(name="Channel " + str(i))
                channel.save()
                channels.append(channel)

        count = 0
        users = []
        while count < user_count:
            next_block = (count / BLOCK_SIZE + 1) * BLOCK_SIZE
            if user_count < next_block:
                next_block = user_count

            with transaction.atomic():
                while count < next_block:
                    user = User(username='user' + str(count), password="password")
                    authentication.generate_token(user)
                    user.save()
                    users.append(user)
                    count += 1
                print count

        count = 0
        while count < event_count:
            next_block = (count / BLOCK_SIZE + 1) * BLOCK_SIZE
            if user_count < next_block:
                next_block = user_count

            with transaction.atomic():
                while count < next_block:
                    event = Event(title="Title " + str(count),
                        description="Description " + str(count),
                        start_time=current_time, end_time=current_time,
                        channel=random.choice(channels),
                        location="Location " + str(count),
                        address="Address " + str(count),
                        lat=100.1234,
                        lon=100.1234,
                        main_picture="uploads/events/7/main_m4c.png"
                    )
                    event.save()
                    for i in range(comment_count):
                        event.create_comment(user=random.choice(users), content="My comment " + str(count))
                    count += 1
                print count
