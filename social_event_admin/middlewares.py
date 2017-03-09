from django.http import HttpResponseRedirect

from social_event.services import authentication
from social_event.models import Admin

class AdminTokenValidateMiddleware(object):
    def process_request(self, request):
        token = self._get_token(request)
        if not token:
            return HttpResponseRedirect("/admin/sign_in")
        request.current_user = authentication.get_user(Admin, token)
        if not request.current_user:
            return HttpResponseRedirect("/admin/sign_in")

        return None

    def _get_token(self, request):
        return request.COOKIES.get('token')
