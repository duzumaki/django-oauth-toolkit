# views.py
from oauth2_provider.views.mixins import OAuthLibMixin
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.compat import login_not_required
from django.utils.decorators import method_decorator
from django import http
from oauthlib.oauth2.rfc8628.pre_configured import DeviceApplicationServer


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_not_required, name="dispatch")
class DeviceAuthorizationView(OAuthLibMixin, View):
    server_class = DeviceApplicationServer

    def post(self, request, *args, **kwargs):
        headers, body, status = self.create_device_authorization_response(request)

        response = {}
        for k, v in headers.items():
            response[k] = v
        response.status_code = status

        return http.JsonResponse(response)
