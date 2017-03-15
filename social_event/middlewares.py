import re, json
from django.http import HttpResponse
from django.core.cache import cache

from social_event.services import authentication
from social_event.models import User, Event

class TokenValidateMiddleware(object):
    def process_request(self, request):
        token = self._get_token(request)
        if not token:
            return HttpResponse(json.dumps({"errors": ["Missing token"]}), status=400, content_type="application/json")
        request.current_user = authentication.get_user(User, token)
        if not request.current_user:
            return HttpResponse(json.dumps({"errors": ["Unauthorized"]}), status=401, content_type="application/json")

        return None

    def _get_token(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        match = authorization_header and re.match(r'^Token (?P<token>.+)$', authorization_header)
        if match:
            return match.group('token')

class RequireEventMiddleware(object):
    def process_request(self, request):
        params = request.GET if request.method == 'GET' else request.POST
        event_id = params.get('event_id')
        if not event_id:
            return HttpResponse(json.dumps({"errors": ["Missing event"]}), status=400, content_type="application/json")

        key = "event.with_id." + str(event_id)
        event = cache.get(key)
        if not event:
            event = Event.objects.filter(id=event_id).first()
            if event:
                cache.set(key, event)

        if not event:
            return HttpResponse(json.dumps({"errors": ["Event not found"]}), status=404, content_type="application/json")

        request.event = event

        return None
