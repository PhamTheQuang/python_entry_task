from django import forms;

from social_event.models import *

class SessionForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128)

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time", "location", "address", "lon", "lat", "main_picture", "channel"]
