import time
from django.db import models, transaction
from social_event.services import authentication

# for obj in User.objects.select_related("item").all():
# prefetch_related
#     print obj.item.name

class AuthenticatableUser(models.Model):
    def __init__(self, *args, **kwargs):
        self.password = kwargs.pop("password", "")
        super(AuthenticatableUser, self).__init__(*args, **kwargs)

    def generate_token(self):
        authentication.generate_token(self)

    def save(self, *args, **kwargs):
        # TODO: Check password is changed
        if self.pk is None:
            authentication.generate_password_digest(self)
        super(AuthenticatableUser, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class AutoTimestampModel(models.Model):
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.create_time = int(time.time())
        super(AutoTimestampModel, self).save(*args, **kwargs)

    def clean_fields(self, exclude=None):
        return super(AutoTimestampModel, self).clean_fields((exclude or []) + ["create_time"])

    class Meta:
        abstract = True

class Admin(AuthenticatableUser):
    username = models.CharField(max_length=128, db_index=True)
    salt = models.CharField(max_length=32)
    password_digest = models.CharField(max_length=128)
    token = models.CharField(max_length=32, blank=True)
    token_expire_time = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return self.username

    class Meta:
        db_table = "admin_tab"
        index_together = [["token", "token_expire_time"]]

def _user_portrait_path(user, filename):
    return "uploads/portraits/{1}_{2}".format(user.id, filename)

class User(AuthenticatableUser):
    username = models.CharField(max_length=128, db_index=True)
    salt = models.CharField(max_length=32)
    password_digest = models.CharField(max_length=128)
    token = models.CharField(max_length=32, blank=True)
    token_expire_time = models.PositiveIntegerField(null=True)
    full_name = models.CharField(max_length=128, blank=True)
    portrait = models.ImageField(upload_to=_user_portrait_path, blank=True)

    def __unicode__(self):
        return self.username

    class Meta:
        db_table = "user_tab"
        index_together = [["token", "token_expire_time"]]

def _event_main_picture_path(event, filename):
    return "uploads/events/{0}/main_{1}".format(event.id, filename)

class Event(AutoTimestampModel):
    title = models.CharField(max_length=128)
    description = models.TextField()
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()
    # channel_id = models.BigIntegerField()
    total_comments = models.BigIntegerField(default=0)
    total_likes = models.BigIntegerField(default=0)
    total_participants = models.BigIntegerField(default=0)
    location = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    lon = models.FloatField()
    lat = models.FloatField()
    main_picture = models.ImageField(upload_to=_event_main_picture_path, blank=True)
    create_time = models.PositiveIntegerField()
    channel = models.ForeignKey('Channel', db_constraint=False)

    def create_comment(self, **kwargs):
        return self._create_interaction(Comment, "total_comments", **kwargs)

    def create_like(self, **kwargs):
        return self._create_interaction(Like, "total_likes", **kwargs)

    def create_participant(self, **kwargs):
        return self._create_interaction(Participant, "total_participants", **kwargs)

    def delete_like(self, like):
        return self._delete_interaction(like, "total_likes")

    def delete_participant(self, participant):
        return self._delete_interaction(participant, "total_participants")

    def _create_interaction(self, klass, attr, **kwargs):
        interaction = klass(event=self, **kwargs)
        interaction.full_clean()
        with transaction.atomic():
            interaction.save()
            setattr(self, attr, getattr(self, attr) + 1)
            self.save()
        return interaction

    def _delete_interaction(self, interaction, attr):
        with transaction.atomic():
            interaction.delete()
            setattr(self, attr, getattr(self, attr) - 1)
            self.save()
        return interaction

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = "event_tab"
        index_together = [
            ["create_time", "start_time", "end_time"],
            ["create_time", "end_time"],
            ["create_time", "channel", "start_time", "end_time"],
            ["create_time", "channel", "end_time"]
        ]

class Channel(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "channel_tab"

def _picture_image_path(picture, filename):
    return "uploads/events/{0}/{1}".format(picture.event_id, filename)

class Picture(models.Model):
    # event_id = models.BigIntegerField()
    image = models.ImageField(upload_to=_picture_image_path)
    event = models.ForeignKey('Event', db_constraint=False, db_index=True)

    class Meta:
        db_table = "picture_tab"

class Comment(AutoTimestampModel):
    content = models.TextField()
    # user_id = models.BigIntegerField()
    # event_id = models.BigIntegerField()
    # reply_comment_id = models.BigIntegerField(null=True)
    create_time = models.PositiveIntegerField()
    event = models.ForeignKey('Event', db_constraint=False, db_index=True)
    user = models.ForeignKey('User', db_constraint=False)
    reply_comment = models.ForeignKey('Comment', db_constraint=False, null=True, blank=True)

    class Meta:
        db_table = "comment_tab"

class Like(AutoTimestampModel):
    # user_id = models.BigIntegerField()
    # event_id = models.BigIntegerField()
    create_time = models.PositiveIntegerField()
    event = models.ForeignKey('Event', db_constraint=False)
    user = models.ForeignKey('User', db_constraint=False)

    class Meta:
        db_table = "like_tab"
        unique_together = [["event", "user"]]

class Participant(AutoTimestampModel):
    # user_id = models.BigIntegerField()
    # event_id = models.BigIntegerField()
    create_time = models.PositiveIntegerField()
    event = models.ForeignKey('Event', db_constraint=False)
    user = models.ForeignKey('User', db_constraint=False)

    class Meta:
        db_table = "participant_tab"
        unique_together = [["event", "user"]]
