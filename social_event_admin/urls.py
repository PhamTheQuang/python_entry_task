from django.conf.urls import patterns, url
from social_event_admin import views

urlpatterns = patterns('',
    url(r'^sign_in$', views.sign_in),
    url(r'^events/new$', views.event_new),
    url('^events\/(\d+)$', views.event),
    url(r'^events$', views.events),
)
