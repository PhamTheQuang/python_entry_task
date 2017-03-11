from django import forms;
from django.forms.models import inlineformset_factory

from datetimewidget.widgets import DateTimeWidget

from social_event.models import *

class SessionForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128)

DATETIME_WIDGET_OPTIONS = {"format": "yyyy-mm-ddThh:ii:ss"}

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time", "location", "address", "lon", "lat", "main_picture", "channel"]
        widgets = {
            'start_time': DateTimeWidget(bootstrap_version=3, options=DATETIME_WIDGET_OPTIONS),
            'end_time': DateTimeWidget(bootstrap_version=3, options=DATETIME_WIDGET_OPTIONS)
        }

PictureFormSet = inlineformset_factory(Event, Picture, fields=('image',))
