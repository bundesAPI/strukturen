import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
from oauth.services import UserProfileService
from settings.search import get_search_client


def home(request):
    """serve 200 at /"""
    return HttpResponse(
        "Hey there! Just another strukturen backend.", content_type="text/plain"
    )


def status(request):
    """serve 200 at /"""
    client = get_search_client()
    return HttpResponse(
        json.dumps({"search": client.info()}), content_type="application/json"
    )


@login_required
def account(request):
    """renders a basic user account view"""
    return TemplateResponse(request, "account.html", {"user": request.user})
