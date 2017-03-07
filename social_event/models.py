from django.db import models

class Admin(models.Model):
    username = models.CharField(max_length=128)
    salt = models.CharField(max_length=32)
    password_digest = models.CharField(max_length=128)
    token = models.CharField(max_length=32, blank=True)
    token_expire_time = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = "admin_tab"

class User(models.Model):
    username = models.CharField(max_length=128)
    salt = models.CharField(max_length=32)
    password_digest = models.CharField(max_length=128)
    token = models.CharField(max_length=32, blank=True)
    token_expire_time = models.PositiveIntegerField(null=True)
    full_name = models.CharField(max_length=128, blank=True)
    portrait = models.CharField(max_length=2086)

    class Meta:
        db_table = "user_tab"

class Event(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()
    channel_id = models.BigIntegerField()
    total_comments = models.BigIntegerField()
    total_likes = models.BigIntegerField()
    total_participants = models.BigIntegerField()
    location = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    lon = models.FloatField()
    lat = models.FloatField()
    main_pictures = models.CharField(max_length=2086, blank=True)
    create_time = models.PositiveIntegerField()

    class Meta:
        db_table = "event_tab"

class Channel(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "event_tab"

class Picture(models.Model):
    event_id = models.BigIntegerField()
    path = models.CharField(max_length=128)

    class Meta:
        db_table = "picture_tab"

class Comment(models.Model):
    content = models.TextField()
    user_id = models.BigIntegerField()
    event_id = models.BigIntegerField()
    reply_comment_id = models.BigIntegerField(null=True)
    create_time = models.PositiveIntegerField()

    class Meta:
        db_table = "comment_tab"

class Like(models.Model):
    user_id = models.BigIntegerField()
    event_id = models.BigIntegerField()
    create_time = models.PositiveIntegerField()

    class Meta:
        db_table = "like_tab"

class Participiant(models.Model):
    user_id = models.BigIntegerField()
    event_id = models.BigIntegerField()
    create_time = models.PositiveIntegerField()

    class Meta:
        db_table = "participant_tab"