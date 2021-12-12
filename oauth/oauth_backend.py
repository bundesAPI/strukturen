from django.contrib.auth import get_user_model
import jwt
from oauth2_provider_jwt.utils import decode_jwt
from oauthlib.common import Request
from rest_framework import exceptions
from oauth2_provider.oauth2_backends import get_oauthlib_core


UserModel = get_user_model()
OAuthLibCore = get_oauthlib_core()


class OAuth2Backend:
    """
    Authenticate against an OAuth2 access token
    """

    def authenticate(self, request=None, **credentials):
        if request is not None:
            if "Authorization" in request.headers:
                hdr = request.headers["Authorization"].split()

                try:
                    payload = decode_jwt(hdr[1])
                except jwt.ExpiredSignatureError:
                    msg = "Signature has expired."
                    raise exceptions.NotAuthenticated(msg)
                except jwt.DecodeError:
                    msg = "Error decoding signature."
                    raise exceptions.NotAuthenticated(msg)
                except (jwt.InvalidTokenError, jwt.InvalidSignatureError):
                    raise exceptions.NotAuthenticated()

                uri, http_method, body, headers = OAuthLibCore._extract_params(request)
                headers["HTTP_AUTHORIZATION"] = " ".join(
                    [hdr[0], payload["access_token"]]
                )
                headers["Authorization"] = " ".join([hdr[0], payload["access_token"]])

                valid, r = OAuthLibCore.server.verify_request(
                    uri, http_method, body, headers, scopes=[]
                )
                if valid:
                    return r.user
        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
