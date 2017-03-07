from django.conf.urls import patterns, include, url
from social_event import views

urlpatterns = patterns('',
    url(r'^users/sign_in$', views.user_sign_in),
    # url(r'^channels$', views.channels),
    # url('^events\/(?P<id>\d+)$', views.event),
    # url(r'^events$', views.events),
    # url('^comments\/(?P<id>\d+)$', views.comment),
    # url(r'^comments$', views.comments),
    # url('^likes\/(?P<id>\d+)$', views.like),
    # url(r'^likes$', views.likes),
    # url('^likes\/(?P<id>\d+)$', views.participant)
    # url(r'^participants$', views.participants)
)
