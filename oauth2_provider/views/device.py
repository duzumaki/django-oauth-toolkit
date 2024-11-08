# views.py
from oauth2_provider.views.mixins import OAuthLibMixin
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.compat import login_not_required
from django.utils.decorators import method_decorator
from django import http
from oauthlib.oauth2.rfc8628.endpoints import DeviceApplicationServer
from oauth2_provider.models import Device, create_device
from oauth2_provider.models import DeviceRequest, DeviceCodeResponse
from urllib.parse import parse_qs


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(login_not_required, name="dispatch")
class DeviceAuthorizationView(OAuthLibMixin, View):
    server_class = DeviceApplicationServer

    def post(self, request, *args, **kwargs):
        headers, data, status = self.create_device_authorization_response(request)

        parsed_body: dict[str, list[str]] = parse_qs(request.body.decode())
        device_request = DeviceRequest(**{k: v[0] for k, v in parsed_body.items()})
        device_response = DeviceCodeResponse(**data)
        create_device(device_request, device_response)
        return http.JsonResponse(data=data, status=status, headers=headers)
