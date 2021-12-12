from django.urls import path, re_path, include


from oauth2_provider import urls as oauth2_provider_urls
import oauth2_provider.views as oauth2_views
from oauth2_provider.views import IntrospectTokenView, JwksInfoView, UserInfoView
from rest_framework_social_oauth2.views import invalidate_sessions

from oauth.views import TokenView

urlpatterns = [
    path(
        "authorize/",
        oauth2_views.AuthorizationView.as_view(
            template_name="oauth/authorization.html"
        ),
        name="authorize",
    ),
    path("token/", TokenView.as_view(), name="token"),
    path("revoke-token/", oauth2_views.RevokeTokenView.as_view(), name="revoke_token"),
    path("invalidate-sessions/", invalidate_sessions, name="invalidate_sessions"),
    path(r"introspect/", IntrospectTokenView.as_view(), name="introspect"),
    re_path(r"^jwks/$", JwksInfoView.as_view(), name="jwks-info"),
    re_path(r"^userinfo/$", UserInfoView.as_view(), name="user-info"),
]

urlpatterns += oauth2_provider_urls.management_urlpatterns
urlpatterns += oauth2_provider_urls.oidc_urlpatterns
