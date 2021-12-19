"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from graphene_django.views import GraphQLView

from settings import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path(r"oauth/", include(("oauth.urls", "oauth"), namespace="oauth2_provider")),
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
