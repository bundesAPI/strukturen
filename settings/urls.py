from django.conf.urls import url
from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from graphene_file_upload.django import FileUploadGraphQLView

from settings.views import home

from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
    path(r"oauth/", include(("oauth.urls", "oauth"), namespace="oauth2_provider")),
    path("", home),
]
if settings.DEBUG:
    urlpatterns += [
        url(
            r"^media/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
