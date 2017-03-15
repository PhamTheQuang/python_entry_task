from django.conf import settings
from django.conf.urls import patterns, include, url, static

urlpatterns = patterns('',
    url(r'^api/', include('social_event.urls')),
    url(r'^admin/', include('social_event_admin.urls')),
)

if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
