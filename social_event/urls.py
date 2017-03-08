from django.conf.urls import patterns, include, url
from social_event import views

urlpatterns = patterns('',
    url(r'^users/sign_in$', views.user_sign_in),
    url(r'^channels$', views.channels),
    url('^events\/(\d+)$', views.event),
    url(r'^events$', views.events),
    url(r'^comments$', views.comments),
    url('^unlikes\/(\d+)$', views.unlike), #id of like, not event.
    url(r'^likes$', views.likes),
    url('^unparticipants\/(\d+)$', views.unparticipate),
    url(r'^participants$', views.participants)
)
