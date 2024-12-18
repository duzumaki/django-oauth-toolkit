# views.py
import json

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
        headers, response, status = self.create_device_authorization_response(request)

        parsed_body: dict[str, list[str]] = parse_qs(request.body.decode())
        device_request = DeviceRequest(client_id=parsed_body["client_id"], scope=parsed_body.get("scope", "openid"))

        if status != 200:
            return http.JsonResponse(data=json.loads(response), status=status, headers=headers)

        device_response = DeviceCodeResponse(**response)
        create_device(device_request, device_response)

        return http.JsonResponse(data=response, status=status, headers=headers)

